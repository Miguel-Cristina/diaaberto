from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

# from .models import Utilizador


# from .forms import Criar_Colab_Form, Editar_Colab_From
from diaabertoapp.models import Colaboracao, UtilizadorTarefa, AuthUser, Utilizador, Tarefa, DiaAberto


def remove_all_space(string):
    return string.replace(" ", "")

class Criar_colab(View):
    template_name = 'criar_colaboracao.html'

    def get(self, request):
        # form = Criar_Colab_Form()
        data_fim1 = DiaAberto.objects.get(pk=1).data_fim
        data_fim = str(data_fim1)
        data_inicio1 = DiaAberto.objects.get(pk=1).data_inicio
        data_inicio = str(data_inicio1)
        return render(request, self.template_name, {
            'data_fim': data_fim,
            'data_inicio': data_inicio,

        })

    def post(self, request):
        '''form_colab = Criar_Colab_Form(request.POST)
        #print(form_register.errors)
        if form_colab.is_valid():
            primeiro_dia = form_colab['primeiro_dia'].value()
            segundo_dia = form_colab['segundo_dia'].value()
            sala_de_aula = form_colab['sala_de_aula'].value()
            percurso = form_colab['percurso'].value()'''
        data_colaboracao = request.POST['data_colaboracao']
        # segundo_dia = request.POST['segundo_dia']
        hora_inicio_colab = remove_all_space(request.POST['hora_inicio_colab'])
        hora_fim_colab = remove_all_space(request.POST['hora_fim_colab'])
        sala_de_aula = request.POST['sala_de_aula']
        percurso = request.POST['percurso']

        if sala_de_aula == "sim":
            sala_de_aula = 1
        else:
            sala_de_aula = 0

        if percurso == "sim":
            percurso = 1
        else:
            percurso = 0
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
        Colaboracao.objects.create(colaborador_id=pk_user.pk, data_colaboracao=data_colaboracao, sala_de_aula=sala_de_aula,
                                   percurso=percurso, hora_inicio_colab=hora_inicio_colab,
                                   hora_fim_colab=hora_fim_colab)
        #user_id.pk
        return redirect('/colaboradores/consultar_colab/')


class Editar_colab(View):
    template_name = 'editar_colaboracao.html'

    def get(self, request,pk):
        obj = Colaboracao.objects.get(pk=pk)
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
        })

    def post(self, request,pk):
        #primeiro_dia = request.POST['primeiro_dia']
        #segundo_dia = request.POST['segundo_dia']
        sala_de_aula = request.POST['sala_de_aula']
        percurso = request.POST['percurso']
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
                                            hora_fim_colab=hora_fim_colab)
        messages.error(request, "Colaboração editada com sucesso!")
        return redirect('/colaboradores/consultar_colab/')


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
        return redirect('/colaboradores/consultar_colab/')


class Consultar_colab(View):
    template_name = 'consultar_colaboracao.html'

    def get(self, request):
        lista_colab3 = []
        user_id=request.user
        print(user_id.pk)
        pk_user = AuthUser.objects.get(pk=user_id.pk).utilizador
        lista_colab_final = Colaboracao.objects.filter(colaborador_id=pk_user.pk)
        lista_tarefa_atrib = Tarefa.objects.filter(colaborador_id=pk_user.pk)
        print(lista_tarefa_atrib)
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
            'lista_colab_final': lista_colab_final,
            'lista_tarefa_atrib': lista_tarefa_atrib,
        })

    def post(self, request):
        post= request.POST
        id=post['del']
        print(id)
        Colaboracao.objects.filter(pk=id).delete()
        return redirect('/colaboradores/consultar_colab/')
    #

class Consultar_tarefa(View):
    template_name = 'consultar_tarefa.html'

    def get(self, request):
        lista_colab3 = []
        user_id=request.user
        # lista_tarefa = UtilizadorTarefa.objects.filter(colaborador_id=user_id.pk)
        lista_tarefa = Tarefa.objects.filter(colaborador_id=user_id.pk)
        print(lista_tarefa)
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
            'lista_tarefa': lista_tarefa,
        })

    def post(self, request):
        post= request.POST
        id=post['del']
        print(id)
        #Colaboracao.objects.filter(pk=id).delete()
        return redirect('/colaboradores/consultar_colab/')