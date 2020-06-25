from datetime import date, time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from diaaberto.utils import render_to_pdf
from diaabertoapp.models import Ementa, Escola, Inscricao, EmentaInscricao, Transporteproprio, Atividade, SessaoAtividade, \
    SessaoAtividadeInscricao, InscricaoGrupo, InscricaoIndividual, TransporteproprioPercursos, AuthUser


def remove_all_space(string):
    return string.replace(" ", "")


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, 'home.html', )


class success(View):
    def get(self, request):
        return render(request, 'home.html', context={'MSG': "Sucesso"})


class CriarInscricaoView(View):
    template_name = 'inscricao.html'

    def get(self, request):
        auth_user = request.user
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        # utilizador = Utilizador.objects.get(pk=auth_user.id)
        if utilizador.utilizadortipo.tipo == "Participante Individual" or \
                utilizador.utilizadortipo.tipo == "Participante em Grupo":
            values = Ementa.objects.all
            escolas = Escola.objects.all
            atividades = Atividade.objects.all
            sessaoatividade = SessaoAtividade.objects.all
            today = date.today()
            age = today.year - utilizador.data_nascimento.year - ((today.month, today.day) < (
                utilizador.data_nascimento.month, utilizador.data_nascimento.day
            ))
            return render(request, self.template_name, {
                'values': values,
                'escolas': escolas,
                'atividades': atividades,
                'sessaoatividade': sessaoatividade,
                'utilizador': utilizador,
                'age': age,
            })
        else:
            return HttpResponse('<h1>Não lhe é permitido aceder a esta página</h1>')

    def post(self, request):
        # --------------------------escola----------------------------------
        escola_escolhida = request.POST['Escola']
        print(escola_escolhida)
        if escola_escolhida != "Escolher":
            if escola_escolhida == 'others':
                nome = request.POST['nome']
                morada = request.POST['morada']
                codigo_postal = request.POST['codigo_postal']
                contacto = request.POST['contacto']
                localidade = request.POST['localidade']
                Escola.objects.create(nome=nome, morada=morada, codigo_postal=codigo_postal, contacto=contacto,
                                      localidade=localidade)
                escola = Escola.objects.get(nome=nome)
            else:
                escola = Escola.objects.get(nome=escola_escolhida)
            # ------------inscricao grupo/individual
            # session user--------------------------------------
            auth_user = request.user
            # utilizador = Utilizador.objects.get(pk=auth_user.id)
            utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
            # session user--------------------------------------
            area_estudos = request.POST['area_estudos']
            ano_estudos = request.POST['ano_estudos']
            inscricao = Inscricao.objects.create(escola=escola, hora_check_in=time(23, 59, 59),
                                                 area_estudos=area_estudos,
                                                 ano_estudos=ano_estudos, utilizador=utilizador)
            radio_value_tipo_part = utilizador.utilizadortipo.tipo
            if radio_value_tipo_part == "Participante em Grupo":
                turma = request.POST['turma']
                total_participantes = request.POST['total_participantes']
                total_professores = request.POST['total_professores']
                InscricaoGrupo.objects.create(total_participantes=total_participantes,
                                              total_professores=total_professores,
                                              turma=turma, inscricao=inscricao)
                participante2 = InscricaoGrupo.objects.get(inscricao=inscricao)
            elif radio_value_tipo_part == "Participante Individual":
                acompanhantes = request.POST['acompanhantes']
                uploaded_file = request.FILES['myfile']
                print("uploaded_file")
                print(uploaded_file)
                fs = FileSystemStorage()
                fs_saved = 'LES/inscricao/static/autorizacao/inscricao' + str(inscricao.id)
                fs.save(fs_saved, uploaded_file)
                InscricaoIndividual.objects.create(autorizacao=0,
                                                   ficheiro_autorizacao=fs_saved,
                                                   acompanhantes=acompanhantes,
                                                   inscricao=inscricao
                                                   )
                participante2 = InscricaoIndividual.objects.get(inscricao=inscricao)
            # ---------refeicao
            n_aluno = request.POST['numero_aluno_normal']
            n_outro = request.POST['numero_outro_normal']
            ementa = Ementa.objects.first()
            EmentaInscricao.objects.create(ementa=ementa, inscricao=inscricao,
                                           numero_aluno_normal=n_aluno,
                                           numero_outro_normal=n_outro
                                           )
            ementainscricao = EmentaInscricao.objects.get(inscricao=inscricao)
            # -----------transporte------------------------------------
            drop_value = request.POST['tipo_transporte']
            trans_para_campus = "nao"
            if drop_value == "autocarro" or drop_value == "comboio":
                trans_para_campus_value = request.POST['QuerTransportePara']
                if trans_para_campus_value == "sim":
                    trans_para_campus = "sim"
            else:
                trans_para_campus = "nao"
            trans_entre_campus_value = request.POST['QuerTransporteEntre']
            if trans_entre_campus_value == 'ida':
                trans_entre_campus = "só ida"
            elif trans_entre_campus_value == 'idavolta':
                trans_entre_campus = "ida e volta"
            else:
                trans_entre_campus = "nao"
            chegada = remove_all_space(request.POST['timepicker-one'])
            partida = remove_all_space(request.POST['timepicker-two'])
            Transporteproprio.objects.create(tipo_transporte=drop_value,
                                             transporte_para_campus=trans_para_campus,
                                             transporte_entre_campus=trans_entre_campus,
                                             hora_chegada=chegada,
                                             hora_partida=partida,
                                             inscricao=inscricao
                                             )
            transporte = Transporteproprio.objects.get(inscricao=inscricao)
            entre_campus_ida = remove_all_space(request.POST['timepicker-three'])
            entre_campus_volta = remove_all_space(request.POST['timepicker-four'])
            if drop_value == "autocarro" or drop_value == "comboio":
                trans_para_campus_value = request.POST['QuerTransportePara']
                if trans_para_campus_value == "sim":
                    destino = request.POST['qual']
                    if drop_value == "autocarro":
                        origem = "estacao autocarros"
                    else:
                        origem = "estacao comboios"
                    TransporteproprioPercursos.objects.create(origem=origem,
                                                              destino=destino,
                                                              hora=chegada,
                                                              transporteproprio=transporte
                                                              )
                    if trans_entre_campus_value == 'ida':
                        if destino == 'penha':
                            destino = 'gambelas'
                        elif destino == 'gambelas':
                            destino = 'penha'
                    TransporteproprioPercursos.objects.create(origem=destino,
                                                              destino=origem,
                                                              hora=partida,
                                                              transporteproprio=transporte
                                                              )
            origementre = ""
            destinoentre = ""
            if trans_entre_campus_value == 'ida' or trans_entre_campus_value == 'idavolta':
                trans_entre_campus = request.POST['transporte_campus']
                if trans_entre_campus == "penha_para_gambelas":
                    origementre = "penha"
                    destinoentre = "gambelas"
                elif trans_entre_campus == "gambelas_para_penha":
                    origementre = "gambelas"
                    destinoentre = "penha"
                TransporteproprioPercursos.objects.create(origem=origementre,
                                                          destino=destinoentre,
                                                          hora=entre_campus_ida,
                                                          transporteproprio=transporte
                                                          )
                if trans_entre_campus_value == 'idavolta':
                    TransporteproprioPercursos.objects.create(origem=destinoentre,
                                                              destino=origementre,
                                                              hora=entre_campus_volta,
                                                              transporteproprio=transporte
                                                              )
            # ----------------------sessao------------------
            row_count = int(request.POST['row_countt'])
            if row_count > 0:
                rows_deleted_count = request.POST['row_deletedd']
                list_deleted = []
                for y in range(int(rows_deleted_count)):
                    list_deleted.append(request.POST['row_deleted_' + str(y)])
                for x in range(row_count):
                    if str(x) not in list_deleted:
                        sessao_actividade_id = request.POST['sessao_atividade_' + str(x)]
                        n_inscritos = request.POST['inscritos_sessao_' + str(x)]
                        sessaoactividade = SessaoAtividade.objects.get(pk=sessao_actividade_id)
                        SessaoAtividadeInscricao.objects.create(sessaoAtividade=sessaoactividade,
                                                                inscricao=inscricao, numero_alunos=n_inscritos
                                                                )
                        if sessaoactividade.sessao.hora < inscricao.hora_check_in:
                            inscricao.hora_check_in = sessaoactividade.sessao.hora
                            inscricao.unidadeorganica_checkin = sessaoactividade.atividade.unidadeorganica
                            inscricao.save()
                        novo_numero_alunos = SessaoAtividade.objects.get(pk=sessao_actividade_id).n_alunos - int(
                            n_inscritos)
                        sessaoactividade.n_alunos = novo_numero_alunos
                        sessaoactividade.save()
                sessao = SessaoAtividadeInscricao.objects.filter(inscricao=inscricao)
                data = {
                    'participante': inscricao,
                    'utilizador': utilizador,
                    'participantetipo': participante2,  # sem erro, if corre sempre
                    'sessao': sessao,
                    'transporte': transporte,
                    'eminsc': ementainscricao,
                }
                email = EmailMessage()
                email.subject = 'Inscricao Dia Aberto'
                email.body = 'Seguem em anexo um pdf com os dados relativos á sua Inscricao'
                email.from_email = settings.EMAIL_HOST_USER
                email.to = [utilizador.email]
                pdf = render_to_pdf(data)
                # preview------------comentar para enviar email----------
                # if pdf:
                #     response = HttpResponse(pdf, content_type='application/pdf')
                #     filename = "PrivacyRequest_%s.pdf" % "1234"
                #     content = "inline; filename='%s'" % filename
                #     response['Content-Disposition'] = content
                #     return response
                # -------------------------------------------------------
                email.attach('inscricao.pdf', pdf.getvalue(), 'application/pdf')
                email.send()
                return render(request, 'inscricao_sucess.html', context={'email': utilizador.email})


class ConsultarInscricaoView(View):
    template_name = 'consultarInscricao.html'

    def get(self, request):
        # session user--------------------------------------
        auth_user = request.user
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        if utilizador.utilizadortipo.tipo == "Participante Individual" or \
                utilizador.utilizadortipo.tipo == "Participante em Grupo" or \
                utilizador.utilizadortipo.tipo == "Administrador" or \
                utilizador.utilizadortipo.tipo == "Coordenador":
            href = {"Minha Inscrição", "Inicio"}
            inscricao = Inscricao.objects.all()
            grupos = InscricaoGrupo.objects.all()
            individual = InscricaoIndividual.objects.all()
            sessoes = SessaoAtividadeInscricao.objects.all()
            transportes = Transporteproprio.objects.all()
            ementainscricao = EmentaInscricao.objects.all()
            ementa = Ementa.objects.first()
            # --------------------------------------------------
            return render(request, self.template_name, {
                'href': href,
                'inscricao': inscricao,
                'grupos': grupos,
                'individual': individual,
                'sessoes': sessoes,
                'utilizador': utilizador,
                'transportes': transportes,
                'ementainscricao': ementainscricao,
                'ementa': ementa
            })
        else:
            return HttpResponse('<h1>Não lhe é permitido aceder a esta página</h1>')

    def post(self, request):
        typee = request.POST['type']
        # 1-apagar inscricao completa;    2-apgar sessao da inscricao
        print("tipo= " + typee)
        if typee == "1":
            insc = Inscricao.objects.get(pk=request.POST['del'])
            sai = SessaoAtividadeInscricao.objects.filter(inscricao=insc)
            for s in sai:
                s.sessaoAtividade.n_alunos = s.sessaoAtividade.n_alunos + s.numero_alunos
                s.sessaoAtividade.save()
                s.delete()
            EmentaInscricao.objects.get(inscricao=insc).delete()
            if insc.utilizador.utilizadortipo.id == 6:
                InscricaoGrupo.objects.get(inscricao=insc).delete()
            elif insc.utilizador.utilizadortipo.id == 1:
                InscricaoIndividual.objects.get(inscricao=insc).delete()
            trans = Transporteproprio.objects.get(inscricao=insc)
            for p in TransporteproprioPercursos.objects.filter(transporteproprio=trans):
                p.delete()
            trans.delete()
            sai.delete()
            insc.delete()
            messages.success(request, "Inscrição apagada com sucesso!")
        elif typee == "2":
            del2 = request.POST['del2']
            sai = SessaoAtividadeInscricao.objects.get(pk=del2)
            sai.sessaoAtividade.n_alunos = sai.sessaoAtividade.n_alunos + sai.numero_alunos
            sai.sessaoAtividade.save()
            sai.delete()
            messages.success(request, "Sessão inscrita apagada com sucesso!")
        return redirect('/inscricao/consultar')


class EditarInscricaoView(View):
    template_name = 'editarinscricao.html'

    def get(self, request, pk):
        # session user--------------------------------------
        auth_user = request.user
        # utilizador = Utilizador.objects.get(pk=auth_user.id)
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        if utilizador.utilizadortipo.tipo == "Participante Individual" or \
                utilizador.utilizadortipo.tipo == "Participante em Grupo":
            if Inscricao.objects.get(pk=pk).utilizador.id == utilizador.id:
                values = Ementa.objects.all
                escolas = Escola.objects.all
                atividades = Atividade.objects.all
                sessaoatividade = SessaoAtividade.objects.all
                today = date.today()
                age = today.year - utilizador.data_nascimento.year - (
                        (today.month, today.day) < (utilizador.data_nascimento.month, utilizador.data_nascimento.day))
                # --------------------------------------------------
                inscricao = Inscricao.objects.get(pk=pk)
                if utilizador.utilizadortipo.id == 6:
                    tipoparticipante = InscricaoGrupo.objects.get(inscricao=inscricao)
                elif utilizador.utilizadortipo.id == 1:
                    tipoparticipante = InscricaoIndividual.objects.get(inscricao=inscricao)
                else:
                    tipoparticipante = ''
                ementainscricao = EmentaInscricao.objects.get(inscricao=inscricao)
                transporteproprio = Transporteproprio.objects.get(inscricao=inscricao)
                percursos = TransporteproprioPercursos.objects.filter(transporteproprio=transporteproprio)
                sessoesinscritas = SessaoAtividadeInscricao.objects.filter(inscricao=inscricao)
                for s in sessoesinscritas:
                    s.sessaoAtividade.n_alunos = s.sessaoAtividade.n_alunos + s.numero_alunos
                    s.sessaoAtividade.save()
                return render(request, self.template_name, {
                    'values': values,
                    'escolas': escolas,
                    'atividades': atividades,
                    'sessaoatividade': sessaoatividade,
                    'utilizador': utilizador,
                    'age': age,

                    'inscricao': inscricao,
                    'participante': tipoparticipante,
                    'refeicao': ementainscricao,
                    'transporte': transporteproprio,
                    'percurso': percursos,
                    'sessoesinscritas': sessoesinscritas,
                })
            else:
                return HttpResponse('<h1>Não lhe é permitido aceder a esta página</h1>')
        else:
            return HttpResponse('<h1>Não lhe é permitido aceder a esta página</h1>')

    def post(self, request, pk):
        inscricao = Inscricao.objects.get(pk=pk)
        escola_escolhida = request.POST['Escola']
        if escola_escolhida == 'others':
            nome = request.POST['nome']
            morada = request.POST['morada']
            codigo_postal = request.POST['codigo_postal']
            contacto = request.POST['contacto']
            localidade = request.POST['localidade']
            Escola.objects.create(nome=nome, morada=morada, codigo_postal=codigo_postal, contacto=contacto,
                                  localidade=localidade)
            escola = Escola.objects.get(nome=nome)
        else:
            escola = Escola.objects.get(nome=escola_escolhida)
        # session user--------------------------------------
        auth_user = request.user
        # utilizador = Utilizador.objects.get(pk=auth_user.id)
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        # session user--------------------------------------
        area_estudos = request.POST['area_estudos']
        ano_estudos = request.POST['ano_estudos']
        inscricao.escola = escola
        inscricao.area_estudos = area_estudos
        inscricao.ano_estudos = ano_estudos
        inscricao.save()

        radio_value_tipo_part = utilizador.utilizadortipo.tipo
        if radio_value_tipo_part == "Participante em Grupo":
            turma = request.POST['turma']
            total_participantes = request.POST['total_participantes']
            total_professores = request.POST['total_professores']
            participante2 = InscricaoGrupo.objects.get(inscricao=inscricao)
            participante2.total_participantes = total_participantes
            participante2.total_professores = total_professores
            participante2.turma = turma
            participante2.save()
        elif radio_value_tipo_part == "Participante Individual":
            acompanhantes = request.POST['acompanhantes']
            uploaded_file = request.FILES['myfile']
            fs = FileSystemStorage()
            fs_saved = 'LES/inscricao/static/autorizacao/inscricao' + str(inscricao.id)
            fs.save(fs_saved, uploaded_file)
            participante2 = InscricaoIndividual.objects.get(inscricao=inscricao)
            participante2.acompanhantes = acompanhantes
            participante2.ficheiro_autorizacao = fs_saved
            participante2.save()
        # ---------refeicao
        n_aluno = request.POST['numero_aluno_normal']
        n_outro = request.POST['numero_outro_normal']
        ementainscricao = EmentaInscricao.objects.get(inscricao=inscricao)
        ementainscricao.numero_aluno_normal = n_aluno
        ementainscricao.numero_outro_normal = n_outro
        ementainscricao.save()
        # -----------transporte------------------------------------
        drop_value = request.POST['tipo_transporte']
        trans_para_campus = "nao"
        if drop_value == "autocarro" or drop_value == "comboio":
            trans_para_campus_value = request.POST['QuerTransportePara']
            if trans_para_campus_value == "sim":
                trans_para_campus = "sim"
        else:
            trans_para_campus = "nao"
        trans_entre_campus_value = request.POST['QuerTransporteEntre']
        if trans_entre_campus_value == 'ida':
            trans_entre_campus = "só ida"
        elif trans_entre_campus_value == 'idavolta':
            trans_entre_campus = "ida e volta"
        else:
            trans_entre_campus = "nao"
        chegada = remove_all_space(request.POST['timepicker-one'])
        partida = remove_all_space(request.POST['timepicker-two'])
        transporte = Transporteproprio.objects.get(inscricao=inscricao)
        transporte.tipo_transporte = drop_value
        transporte.transporte_para_campus = trans_para_campus
        transporte.transporte_entre_campus = trans_entre_campus
        transporte.hora_chegada = chegada
        transporte.hora_partida = partida
        transporte.save()

        entre_campus_ida = remove_all_space(request.POST['timepicker-three'])
        entre_campus_volta = remove_all_space(request.POST['timepicker-four'])
        if drop_value == "autocarro" or drop_value == "comboio":
            trans_para_campus_value = request.POST['QuerTransportePara']
            if trans_para_campus_value == "sim":
                destino = request.POST['qual']
                percurso = TransporteproprioPercursos.objects.filter(transporteproprio=transporte)
                percurso.delete()
                if drop_value == "autocarro":
                    origem = "estacao autocarros"
                else:
                    origem = "estacao comboios"
                TransporteproprioPercursos.objects.create(origem=origem,
                                                          destino=destino,
                                                          hora=chegada,
                                                          transporteproprio=transporte
                                                          )
                if trans_entre_campus_value == 'ida':
                    if destino == 'penha':
                        destino = 'gambelas'
                    elif destino == 'gambelas':
                        destino = 'penha'
                TransporteproprioPercursos.objects.create(origem=destino,
                                                          destino=origem,
                                                          hora=partida,
                                                          transporteproprio=transporte
                                                          )
        origementre = ""
        destinoentre = ""
        if trans_entre_campus_value == 'ida' or trans_entre_campus_value == 'idavolta':
            trans_entre_campus = request.POST['transporte_campus']
            percurso = TransporteproprioPercursos.objects.filter(transporteproprio=transporte)
            if trans_entre_campus == "penha_para_gambelas":
                origementre = "penha"
                destinoentre = "gambelas"
            elif trans_entre_campus == "gambelas_para_penha":
                origementre = "gambelas"
                destinoentre = "penha"
            TransporteproprioPercursos.objects.create(origem=origementre,
                                                      destino=destinoentre,
                                                      hora=entre_campus_ida,
                                                      transporteproprio=transporte
                                                      )
            if trans_entre_campus_value == 'idavolta':
                TransporteproprioPercursos.objects.create(origem=destinoentre,
                                                          destino=origementre,
                                                          hora=entre_campus_volta,
                                                          transporteproprio=transporte
                                                          )
        # ----------------------sessao------------------
        sessoesinscritas = SessaoAtividadeInscricao.objects.filter(inscricao=inscricao)
        for sai in sessoesinscritas:
            sai.sessaoAtividade.n_alunos = sai.sessaoAtividade.n_alunos + sai.numero_alunos
            sai.sessaoAtividade.save()
            sai.delete()
        row_count = int(request.POST['row_countt'])
        if row_count > 0:
            rows_deleted_count = request.POST['row_deletedd']
            list_deleted = []
            for y in range(int(rows_deleted_count)):
                list_deleted.append(request.POST['row_deleted_' + str(y)])
            for x in range(row_count):
                if str(x) not in list_deleted:
                    sessao_actividade_id = request.POST['sessao_atividade_' + str(x)]
                    n_inscritos = request.POST['inscritos_sessao_' + str(x)]
                    sessaoactividade = SessaoAtividade.objects.get(pk=sessao_actividade_id)
                    SessaoAtividadeInscricao.objects.create(sessaoAtividade=sessaoactividade,
                                                            inscricao=inscricao, numero_alunos=n_inscritos
                                                            )
                    if sessaoactividade.sessao.hora < inscricao.hora_check_in:
                        inscricao.hora_check_in = sessaoactividade.sessao.hora
                        inscricao.unidadeorganica_checkin = sessaoactividade.atividade.unidadeorganica
                        inscricao.save()
                    novo_numero_alunos = SessaoAtividade.objects.get(pk=sessao_actividade_id).n_alunos - int(
                        n_inscritos)
                    sessaoactividade.n_alunos = novo_numero_alunos
                    sessaoactividade.save()
            sessao = SessaoAtividadeInscricao.objects.filter(inscricao=inscricao)
            data = {
                'participante': inscricao,
                'utilizador': utilizador,
                'participantetipo': participante2,  # sem erro, if corre sempre
                'sessao': sessao,
                'transporte': transporte,
                'eminsc': ementainscricao,
            }
            email = EmailMessage()
            email.subject = 'Inscricao Dia Aberto'
            email.body = 'Seguem em anexo um pdf com os dados relativos á sua Inscricao'
            email.from_email = settings.EMAIL_HOST_USER
            email.to = [utilizador.email]
            pdf = render_to_pdf(data)
            # preview------------comentar para enviar email----------
            # if pdf:
            #     response = HttpResponse(pdf, content_type='application/pdf')
            #     filename = "PrivacyRequest_%s.pdf" % "1234"
            #     content = "inline; filename='%s'" % filename
            #     response['Content-Disposition'] = content
            #     return response
            # -------------------------------------------------------
            email.attach('inscricao.pdf', pdf.getvalue(), 'application/pdf')
            email.send()
            messages.success(request, "Utilizador editado com sucesso!")
            return redirect('/inscricao/consultar')
