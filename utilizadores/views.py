import re

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View

from diaabertoapp.models import Utilizador, UtilizadorTipo, Departamento, UnidadeOrganica, UnidadeorganicaDepartamento, \
    AuthUser
from .forms import RegisterForm


class register(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegisterForm()
        utilizadortipo = UtilizadorTipo.objects.all
        departamento = Departamento.objects.all
        unidadeorganica = UnidadeOrganica.objects.all
        unidadeorganica_dep = UnidadeorganicaDepartamento.objects.all
        all_users = Utilizador.objects.all
        return render(request, self.template_name, {
            'form': form,
            'utilizadortipo': utilizadortipo,
            'departamento': departamento,
            'unidadeorganica': unidadeorganica,
            'unidadeorganica_dep': unidadeorganica_dep,
            'all_users': all_users,
        })

    def post(self, request):
        form_register = RegisterForm(request.POST)
        # form_epi = EpiForm()
        # form_prato = PratoForm(request.POST)
        print(form_register.errors)
        if form_register.is_valid():
            # regex = '\w[\w\.-]*@\w[\w\.-]+\.\w+'
            # print("dasd")
            # print(form_register.errors)
            utilizadortipo_value = request.POST['utilizadortipo']
            utilizadortipo = UtilizadorTipo.objects.get(tipo=utilizadortipo_value)
            # email = form_register['email'].value()
            email = request.POST['email']
            print(email)
            # password_digest = form_register['password_digest'].value()
            password_digest = request.POST['password_digest']
            # password_conf = form_register['password_conf'].value()
            password_conf = request.POST['password_conf']
            # nome = form_register['nome'].value()
            nome = request.POST['nome']
            data_nascimento = request.POST['data_nascimento']
            # numero_telemovel = form_register['numero_telemovel'].value()
            numero_telemovel = request.POST['numero_telemovel']
            # cartao_cidadao = form_register['cartao_cidadao'].value()
            cartao_cidadao = request.POST['cartao_cidadao']
            # deficiencias = form_register['deficiencias'].value()
            deficiencias = request.POST['deficiencias']
            # permitir_localizacao = form_register['permitir_localizacao'].value()
            permitir_localizacao = request.POST['permitir_localizacao']
            if permitir_localizacao == "sim":
                permitir_localizacao = 1
            else:
                permitir_localizacao = 0
            # utilizar_dados_pessoais = form_register['utilizar_dados_pessoais'].value()
            utilizar_dados_pessoais = request.POST['utilizar_dados_pessoais']
            if utilizar_dados_pessoais == "sim":
                utilizar_dados_pessoais = 1
            else:
                utilizar_dados_pessoais = 0

            print(utilizadortipo_value)
            if utilizadortipo_value == "Participante Individual" or utilizadortipo_value == "Participante em Grupo":
                unidadeorganica = None
                departamento = None
                validado = 1
            else:
                validado = 0
                unidadeorganica1 = request.POST['unidadeorganica']
                print(unidadeorganica1)
                unidadeorganica = UnidadeOrganica.objects.get(nome=unidadeorganica1)
                if unidadeorganica1 == "Escola Superior de Gestão, Hotelaria e Turismo" or unidadeorganica1 == "Faculdade de Economia" or unidadeorganica1 == "Departamento de Ciências Biomédicas e Medicina":
                    departamento = None
                    print("noneeeee")
                else:
                    if unidadeorganica1 == "Escola Superior de Educação e Comunicação":
                        departamento = request.POST['departamento_esc']
                        print(departamento)
                        departamento = Departamento.objects.get(nome=departamento)
                    if unidadeorganica1 == "Escola Superior de Saúde":
                        departamento = request.POST['departamento_ess']
                        print(departamento)
                        departamento = Departamento.objects.get(nome=departamento)
                    if unidadeorganica1 == "Escola Superior de Engenharia":
                        departamento = request.POST['departamento_ese']
                        print(departamento)
                        departamento = Departamento.objects.get(nome=departamento)
                    if unidadeorganica1 == "Faculdade de Ciências Humanas e Sociais":
                        departamento = request.POST['departamento_fchs']
                        print(departamento)
                        departamento = Departamento.objects.get(nome=departamento)
                    if unidadeorganica1 == "Faculdade de Ciências e Tecnologia":
                        departamento = request.POST['departamento_fct']
                        print(departamento)
                        departamento = Departamento.objects.get(nome=departamento)

            print(unidadeorganica)
            # departamento = request.POST['departamento']
            print(departamento)
            # unidadeorganica = UnidadeOrganica.objects.get(nome=unidadeorganica)
            # departamento = request.POST['departamento']
            # departamento = Departamento.objects.get(nome=departamento)

            # erros--------------------------------------------------------------------------------
            # all_users = Utilizador.objects.all
            # users_emails = all_users.email
            # print(all_users)
            # for all_emails in all_users:
            #     if all_emails.email == email:
            #         messages.error(request, "O email já existe na base de dados")
            #         return redirect('/utilizadores/register/')

            if len(password_digest) < 5:
                messages.error(request, "a password é demasiado pequena")
                return redirect('/utilizadores/register/')

            if password_digest != password_conf:
                messages.error(request, "As passwords não coincidem")
                return redirect('/utilizadores/register/')

            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex, email)):
                print("Valid Email")
            else:
                messages.error(request, "O email nao tem o formato apropriado")
                return redirect('/utilizadores/register/')

            if len(numero_telemovel) != 9:
                messages.error(request, "O numero de telemovel deve conter 9 algarismos")
                return redirect('/utilizadores/register/')

            if len(cartao_cidadao) != 8:
                messages.error(request, "O numero do cartao de cidadão deve conter 8 algarismos")
                return redirect('/utilizadores/register/')
            # ------------------------------------------------------------------------------

            Utilizador.objects.create(utilizadortipo=utilizadortipo, email=email,
                                      nome=nome, data_nascimento=data_nascimento, numero_telemovel=numero_telemovel,
                                      cartao_cidadao=cartao_cidadao, deficiencias=deficiencias,
                                      permitir_localizacao=permitir_localizacao,
                                      utilizar_dados_pessoais=utilizar_dados_pessoais,
                                      unidadeorganica=unidadeorganica, departamento=departamento, validado=validado)
            obj_user = Utilizador.objects.get(email=email)
            User.objects.create_user(username=email, password=password_digest, email=email)
            AuthUser.objects.filter(username=email).update(utilizador=obj_user)
            """escola = Escola.objects.get(nome=nome)
            Inscricao.objects.create(escola=escola)
            inscricao = Inscricao.objects.get(escola=escola)

            if form_prato.is_valid():
                radio_value = form_prato.cleaned_data.get("prato")
                prato = Prato.objects.get(tipo=radio_value)

                ementa = Ementa.objects.all().first()
                EmentaPratoInscricao.objects.create(ementa=ementa, prato=prato, inscricao=inscricao)

            return redirect('/inscricao/home')"""
        return redirect('/utilizadores/login')


def logout_request(request):
    logout(request)
    messages.info(request, "Terminou a sessão com sucesso")
    return redirect('/utilizadores/login')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            utilizador_val = Utilizador.objects.get(email=username)
            if utilizador_val.validado == 1:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "O utilizador não está validado")
        else:
            messages.error(request, "Email ou Password inválida")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def success(request):
    context = {}
    context['user'] = request.user
    return render(request=request,
                  template_name="success.html",
                  context={})


class Consultar_user(View):
    template_name = 'consultar_utilizador.html'

    def get(self, request):
        queryset = Utilizador.objects.all()


        authuser = request.user
        utilizador = AuthUser.objects.get(pk=authuser.pk).utilizador

        context = {
            "object_list": queryset,
            "utilizador": utilizador
        }
        return render(request, "consultar_utilizador.html", context)

    def post(self, request):
        post = request.POST
        type = post['type']
        if type == "1":
            id = post['del']
            print(id)
            Utilizador.objects.get(pk=id).delete()
            messages.add_message(request, messages.WARNING, "Utilizador APAGADO com sucesso")
        elif type == "0":
            print("GGGGGGGGGGGGG")
            id = post['val']
            user = Utilizador.objects.get(pk=id)
            print(user.validado)
            user.validado = 1
            user.save()
            print(user.validado)

        return redirect('/utilizadores/consultar_utilizadores/')


class Editar_user(View):
    template_name = 'editar_utilizador.html'

    def get(self, request, pk):
        obj = Utilizador.objects.get(pk=pk)
        form = RegisterForm
        data_nascimento = Utilizador.objects.get(pk=pk).data_nascimento
        email = Utilizador.objects.get(pk=pk).email
        nome = Utilizador.objects.get(pk=pk).nome
        numero_telemovel = Utilizador.objects.get(pk=pk).numero_telemovel
        cartao_cidadao = Utilizador.objects.get(pk=pk).cartao_cidadao
        deficiencias = Utilizador.objects.get(pk=pk).deficiencias
        permitir_localizacao = Utilizador.objects.get(pk=pk).permitir_localizacao
        utilizar_dados_pessoais = Utilizador.objects.get(pk=pk).utilizar_dados_pessoais

        return render(request, self.template_name, {
            'obj': obj,
            'form': form,
            'data_nascimento': data_nascimento,
            'email': email,
            'nome': nome,
            'numero_telemovel': numero_telemovel,
            'cartao_cidadao': cartao_cidadao,
            'deficiencias': deficiencias,
            'permitir_localizacao': permitir_localizacao,
            'utilizar_dados_pessoais': utilizar_dados_pessoais,

        })

    def post(self, request, pk):

        email = request.POST['email']
        nome = request.POST['nome']
        numero_telemovel = request.POST['numero_telemovel']
        cartao_cidadao = request.POST['cartao_cidadao']
        # deficiencias = request.POST['deficiencias']

        permitir_localizacao = request.POST['permitir_localizacao']
        if permitir_localizacao == "sim":
            permitir_localizacao = 1
        else:
            permitir_localizacao = 0
        utilizar_dados_pessoais = request.POST['utilizar_dados_pessoais']
        if utilizar_dados_pessoais == "sim":
            utilizar_dados_pessoais = 1
        else:
            utilizar_dados_pessoais = 0

        messages.add_message(request, messages.SUCCESS, "Utilizador EDITADO com sucesso")



        # ------------------------------------------------------------------------------

        Utilizador.objects.filter(pk=pk).update(
            nome=nome, email=email,
            numero_telemovel=numero_telemovel,
            cartao_cidadao=cartao_cidadao,
            permitir_localizacao=permitir_localizacao,
            utilizar_dados_pessoais=utilizar_dados_pessoais,
        )

        return redirect('/utilizadores/consultar_utilizadores')


# def get_object(self):
#        id_ = self.kwargs.get("id")
#       return get_object_or_404 (Utilizador, id=id_)


#  def password_change(request):
#   if request.method == 'POST':
#      form = PasswordChangeForm(request.user, request.POST)
#     if form.is_valid():
#        user = form.save()
#       update_session_auth_hash(request, user)
#      messages.success(request, 'Your password was successfully updated!')
#     return redirect('change_password')
# else:
#   messages.error(request, 'Please correct the error below.')
#   else:
#      form = PasswordChangeForm(request.user)
# return render(request, 'password_change.html', {
#    'form': form
# })
#
# def password_change_done(request):
# messages.info(request, "Password changed")
# return render(request, 'password_change_done.html')


#
class Validar_user(View):
    template_name = ''

    def get(self, request, pk):
        obj = Utilizador.objects.get(pk=pk)
        form = RegisterForm
        validado = Utilizador.objects.get(pk=pk).validado

        return render(request, self.template_name, {
            'obj': obj,
            'form': form,
            'validado': validado,

        })

    def post(self, request, pk):

        email = request.POST['email']
        nome = request.POST['nome']
        validado = request.POST['validado']
        if validado == "NULL":
            validado = 1
        else:
            validado = 0

        messages.add_message(request, messages.SUCCESS, "Utilizador Validado com sucesso")

        Utilizador.objects.filter(pk=pk).update(
            nome=nome, email=email,
            validado=validado,
        )

        return redirect('/utilizadores/consultar_utilizadores')
