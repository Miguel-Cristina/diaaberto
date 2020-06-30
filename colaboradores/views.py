import time
from datetime import timedelta

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

# from .models import Utilizador


# from .forms import Criar_Colab_Form, Editar_Colab_From
from diaabertoapp.models import Colaboracao, AuthUser, Utilizador, Tarefa, DiaAberto


def remove_all_space(string):
    return string.replace(" ", "")

class Criar_colab(View):
    template_name = 'criar_colaboracao.html'

    def get(self, request):
        # form = Criar_Colab_Form()
        auth_user = request.user
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        if utilizador.utilizadortipo.tipo == "Colaborador":
            data_fim1 = DiaAberto.objects.get(pk=1).data_fim
            data_fim = str(data_fim1)
            data_inicio1 = DiaAberto.objects.get(pk=1).data_inicio
            data_inicio = str(data_inicio1)
            return render(request, self.template_name, {
                'data_fim': data_fim,
                'data_inicio': data_inicio,
                'utilizador': utilizador
            })
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')

    def post(self, request):
        data_colaboracao = request.POST['data_colaboracao']
        # segundo_dia = request.POST['segundo_dia']
        hora_inicio_colab = remove_all_space(request.POST['hora_inicio_colab'])
        hora_fim_colab = remove_all_space(request.POST['hora_fim_colab'])
        sala_de_aula = request.POST['sala_de_aula']
        percurso = request.POST['percurso']
        outro = request.POST['outro']

        if sala_de_aula == "sim":
            sala_de_aula = 1
        else:
            sala_de_aula = 0

        if percurso == "sim":
            percurso = 1
        else:
            percurso = 0

        if outro == "sim":
            outro = 1
        else:
            outro = 0
        '''if form_colab.is_valid():
            primeiro_dia = form_colab['primeiro_dia'].value()
            segundo_dia = form_colab['segundo_dia'].value()
            sala_de_aula = form_colab['sala_de_aula'].value()
            percurso = form_colab['percurso'].value()
        '''
        user_id=request.user
        #print(user_id.utilizadores)
        pk_user=AuthUser.objects.get(pk=user_id.pk).utilizador#################
        print(pk_user.pk)
        messages.error(request, "Colaboração criada com sucesso!")
        #outras = 1
        Colaboracao.objects.create(colaborador_id=pk_user.pk, data_colaboracao=data_colaboracao, sala_de_aula=sala_de_aula,
                                   percurso=percurso, hora_inicio_colab=hora_inicio_colab,
                                   hora_fim_colab=hora_fim_colab, outras=outro)
        #user_id.pk
        return redirect('/colaboradores/consultar/')


class Editar_colab(View):
    template_name = 'editar_colaboracao.html'

    def get(self, request,pk):
        auth_user = request.user
        utilizador = AuthUser.objects.get(pk=auth_user.pk).utilizador
        obj = Colaboracao.objects.get(pk=pk)
        if utilizador.utilizadortipo.tipo == "Colaborador" and obj.colaborador.id == utilizador.id:
            data_colaboracao1 = Colaboracao.objects.get(pk=pk).data_colaboracao
            data_colaboracao = str(data_colaboracao1)
            inicio_colab1 = Colaboracao.objects.get(pk=pk).hora_inicio_colab
            inicio_colab = str(inicio_colab1)
            fim_colab1 = Colaboracao.objects.get(pk=pk).hora_fim_colab
            fim_colab = str(fim_colab1)

            print(inicio_colab)
            inicio_colab= inicio_colab[:-3]
            fim_colab = fim_colab[:-3]
            print(inicio_colab)
            # form = Editar_Colab_Form()
            # form = Editar_Colab_Form(instance=Utilizador.objects.get(pk=3))
            data_fim1 = DiaAberto.objects.get(pk=1).data_fim
            data_fim = str(data_fim1)
            data_inicio1 = DiaAberto.objects.get(pk=1).data_inicio
            data_inicio = str(data_inicio1)
            return render(request, self.template_name, {
                # 'form': form,
                'obj': obj,
                'data_fim': data_fim,
                'data_inicio': data_inicio,
                'data_colaboracao': data_colaboracao,
                'inicio_colab': inicio_colab,
                'fim_colab': fim_colab,
                'utilizador': utilizador
            })
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')

    def post(self, request,pk):
        #primeiro_dia = request.POST['primeiro_dia']
        #segundo_dia = request.POST['segundo_dia']
        sala_de_aula = request.POST['sala_de_aula']
        percurso = request.POST['percurso']
        outro = request.POST['outro']
        #if primeiro_dia == "sim":
         #   primeiro_dia = 1
        #else:
         #   primeiro_dia = 0

        #if segundo_dia == "sim":
         #   segundo_dia = 1
        #else:
         #   segundo_dia = 0

        if sala_de_aula == "sim":
            sala_de_aula = 1
        else:
            sala_de_aula = 0

        if percurso == "sim":
            percurso = 1
        else:
            percurso = 0

        if outro == "sim":
            outro = 1
        else:
            outro = 0

        '''if form_colab.is_valid():
         primeiro_dia = form_colab['primeiro_dia'].value()
            segundo_dia = form_colab['segundo_dia'].value()
         sala_de_aula = form_colab['sala_de_aula'].value()
            percurso = form_colab['percurso'].value()
        '''
        data_colaboracao = request.POST['data_colaboracao']
        hora_inicio_colab = remove_all_space(request.POST['hora_inicio_colab'])
        hora_fim_colab = remove_all_space(request.POST['hora_fim_colab'])
        Colaboracao.objects.filter(pk=pk).update(data_colaboracao=data_colaboracao, sala_de_aula=sala_de_aula,
                                            percurso=percurso, hora_inicio_colab=hora_inicio_colab,
                                            hora_fim_colab=hora_fim_colab, outras=outro)
        messages.error(request, "Colaboração editada com sucesso!")
        return redirect('/colaboradores/consultar/')


class Apagar_colab(View):
    template_name = 'apagar_colaboracao.html'

    def get(self, request):
        # obj = Utilizador.objects.get(pk=3)
        # form = Editar_Colab_Form()
        # form = Editar_Colab_Form(instance=Utilizador.objects.get(pk=3))
        return render(request, self.template_name, {
            # 'form': form,
            # 'obj': obj,
        })

    def post(self, request):
        # Utilizador.objects.filter(pk=3).update(primeiro_dia=None, segundo_dia=None,
        #                                        sala_de_aula=None, percurso=None)
        return redirect('/colaboradores/consultar/')


class Consultar_colab(View):
    template_name = 'consultar_colaboracao.html'

    def get(self, request):
        lista_colab3 = []
        user_id=request.user
        print(user_id.pk)
        pk_user = AuthUser.objects.get(pk=user_id.pk).utilizador
        if pk_user.utilizadortipo.tipo == "Colaborador":
            lista_colab_final = Colaboracao.objects.filter(colaborador_id=pk_user.pk)
            lista_tarefa_atrib = Tarefa.objects.filter(coolaborador=pk_user.pk)
            print(lista_colab_final)
            for l in lista_colab_final:
                #print(l.tarefa_atribuida)
                Colaboracao.objects.filter(pk=l.id).update(tarefa_atribuida=0)

            lista_colab_final1 = Colaboracao.objects.filter(colaborador_id=pk_user.pk)
            for l1 in lista_colab_final1:
                print(l1.tarefa_atribuida)

            for y in lista_colab_final1:
                #Colaboracao.objects.filter(pk=y.id).update(tarefa_atribuida=0)
                for x in lista_tarefa_atrib:
                    hora_tarefa = timedelta(seconds=((x.horario.hour * 3600) + (x.horario.minute * 60) + x.horario.second))
                    hora_inicio_c = timedelta(seconds=((y.hora_inicio_colab.hour * 3600) + (y.hora_inicio_colab.minute * 60) + y.hora_inicio_colab.second))
                    hora_fim_c = timedelta(seconds=((y.hora_fim_colab.hour * 3600) + (y.hora_fim_colab.minute * 60) + y.hora_fim_colab.second))
                    if y.data_colaboracao == x.dia and hora_inicio_c <= hora_tarefa and hora_fim_c >= hora_tarefa:
                        Colaboracao.objects.filter(pk=y.id).update(tarefa_atribuida=1)
            #time.sleep(5)

            lista_colab_final2 = Colaboracao.objects.filter(colaborador_id=pk_user.pk)
            for l2 in lista_colab_final2:
                print(l2.tarefa_atribuida)
            # for x in lista_colab:
            #     lista_colab3.append(str(x.data_colaboracao))
            #     lista_colab_final =  zip(lista_colab, lista_colab3)
            #hora_str1 = Colaboracao.objects.get(pk=1).hora_inicio_colab
            #hora_str = str(hora_str1)
            #print(lista_colab)
            return render(request, self.template_name, {
                # 'form': form,
                #'lista_colab': lista_colab,
                #'hora_str': hora_str,
                #'lista_colab3': lista_colab3,
                'lista_colab_final': lista_colab_final2,
                'lista_tarefa_atrib': lista_tarefa_atrib,
                'utilizador': pk_user
            })
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')

    def post(self, request):
        post= request.POST
        id=post['del']
        print(id)
        Colaboracao.objects.filter(pk=id).delete()
        return redirect('/colaboradores/consultar/')
    #

class Consultar_tarefa(View):
    template_name = 'consultar_tarefa.html'

    def get(self, request):
        lista_colab3 = []
        user_id=request.user
        pk_user = AuthUser.objects.get(pk=user_id.pk).utilizador
        if pk_user.utilizadortipo.tipo == "Colaborador":
            # lista_tarefa = UtilizadorTarefa.objects.filter(colaborador_id=user_id.pk)
            lista_tarefa = Tarefa.objects.filter(coolaborador=user_id.pk)
            # test = Tarefa.grupo.all()

            # results = Staff.objects.filter(pk=1)
            # grupos_m=[]
            # for y in lista_tarefa:
            #     grupos_m.append(list(y.grupo.all()))
            #     grupos_final=zip(lista_tarefa,grupos_m)
            #
            #
            # for x,y in grupos_final:
            #     print(x.tipo_tarefa)
            #     print(y)
            #
            # lst1 = ['a', 'b', 'c']
            # lst2 = ['a', 'b', 'c']
            # grp= zip(lst1,lst2)
            # for x in lista_colab:
            #     lista_colab3.append(str(x.data_colaboracao))
            #     lista_colab_final =  zip(lista_colab, lista_colab3)
            #hora_str1 = Colaboracao.objects.get(pk=1).hora_inicio_colab
            #hora_str = str(hora_str1)
            #print(lista_colab)
            return render(request, self.template_name, {
                # 'form': form,
                # 'grp': grp,
                # 'grupos': grupos_m,
                # 'tarefa_id': lista_tarefa,
                'lista_tarefa': lista_tarefa,
                'utilizador': pk_user
            })
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')

    def post(self, request):
        post= request.POST
        id=post['del']
        print(id)
        #Colaboracao.objects.filter(pk=id).delete()
        return redirect('/colaboradores/consultar/')