from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.deletion import ProtectedError
from django.db.models import Count
from .models import Dia,SessaoAtividadeInscricao, Prato, Ementa, DiaAberto, Edificio, Atividade, Campus, UnidadeOrganica, Departamento, Tematica, Percurso, Transporte, TransporteUniversitarioHorario, Horario, TipoAtividade,Tarefa, PublicoAlvo, Sala, MaterialQuantidade, Sessao, SessaoAtividade, Utilizador, UtilizadorTipo, UtilizadorParticipante, Notificacao, Colaboracao
from .forms import CampusForm, AtividadeForm, EmentaForm, PratoForm, MaterialQuantidadeForm ,DiaabertoForm, TransporteUniversitarioHorarioForm, SessaoAtividadeForm, TransporteForm, PercursoForm, HorarioForm, MaterialFormSet, TarefaForm, SessoesForm, SessaoFormSet, PublicoAlvoForm, TematicasForm, TipoAtividadeForm, CampusForm, EdificioForm, SalaForm, UnidadeOrganicaForm, DepartamentoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from datetime import date, timedelta, datetime
#from django.db import connection
#========================================================================================================================
#Erro 500 
#========================================================================================================================
def error_500(request):
    return render(request, 'diaabertoapp/error_500.html')

#========================================================================================================================
#Erro 404
#========================================================================================================================
def error_404(request):
    return render(request, 'diaabertoapp/error_404.html')

#========================================================================================================================
#Login request
#Reedireciona para a pagina login.html se nenhum utilizador estiver autentificado
#Reedireciona para a pagina index.html se o utilizador autentificar com sucesso
#========================================================================================================================
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index/')
            else:
                messages.error(request, "Email ou password inválidos.")
        else:
            print(form.errors.as_text)
            messages.error(request, "Email ou password inválidos.")
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = "input"
    form.fields['username'].widget.attrs['type'] = "email"
    form.fields['password'].widget.attrs['class'] = "input"
    return render(request, 'diaabertoapp/login.html', {"form": form})

#========================================================================================================================
#Logout request
#Termina a sessao do utilizador
#Reedireciona para o login
#========================================================================================================================
def logout_request(request):
    logout(request)
    messages.info(request, "Sessão terminada. Até breve!")
    return redirect('/login')
#========================================================================================================================
#Index
#Reedireciona para a pagina inicial
#========================================================================================================================
def index(request):
    utilizador = ''
    notificacoes = Notificacao.objects.none()
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')

    count_notificacoes = 0 
    for x in notificacoes:
        if(x.visto == False):
            count_notificacoes = count_notificacoes + 1

    diaaberto = DiaAberto.objects.first()
    if diaaberto is None:
        return HttpResponseRedirect('/configurardiaaberto')

    return render(request, 'diaabertoapp/index.html', {'count_notificacoes':count_notificacoes,'utilizador':utilizador,'notificacoes':notificacoes,'diaaberto':diaaberto})
#========================================================================================================================
#Administrador
#Reedireciona para a pagina do administrador e das configurações
#========================================================================================================================
def administrador(request):
    return render(request, 'diaabertoapp/administrador.html', {})
#========================================================================================================================
#Configuracao das atividades
#Reedireciona para a pagina das configuracoes das atividades se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configuraratividades(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    sessoes = Sessao.objects.all()
    tipos = TipoAtividade.objects.all()
    publicos = PublicoAlvo.objects.all()
    temas = Tematica.objects.all()
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'tipo':
        if sort == 'asc':
            tipos = tipos.order_by(order_by)
        else:
            sorter = '-' + order_by
            tipos = tipos.order_by(sorter)
    elif order_by == 'tema':
        if sort == 'asc':
            temas = temas.order_by(order_by)
        else:
            sorter = '-' + order_by
            temas = temas.order_by(sorter)
    elif order_by == 'publico':
        if sort == 'asc':
            publicos = publicos.order_by('nome')
        else:
            sorter = '-' + order_by
            publicos = publicos.order_by('-nome')
    elif order_by == 'sessao':
        if sort == 'asc':
            sessoes = sessoes.order_by('hora')
        else:
            sessoes = sessoes.order_by('-hora')


    #END order_by

    return render(request, 'diaabertoapp/configuraratividades.html', {'notificacoes':notificacoes,'utilizador':utilizador,'sessoes':sessoes, 'temas':temas, 'tipos':tipos, 'publicos':publicos,'order_by':order_by, 'sort':sort})
#========================================================================================================================
#Configuracao das espacos
#Reedireciona para a pagina das configuracoes dos espacos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurarespacos(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    #BEGIN filter_by_campus
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
        salas = salas.filter(edificio__campus=campus_query)
        campus = campus.filter(id=campus_query)
        edificios = edificios.filter(campus=campus_query)
    #END filter_by_campus
    #BEGIN filter_by_edificio
    edificio_query = request.GET.get('edificio')
    if edificio_query !='' and edificio_query is not None:
        salas = salas.filter(edificio=edificio_query)
        edificios = edificios.filter(id=edificio_query)
    #END filter_by_edificio
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        salas = salas.filter(identificacao__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'campus':
        if sort == 'asc':
            salas = salas.order_by('edificio__campus__nome')
        else:
            salas = salas.order_by('-edificio__campus__nome')
    elif order_by == 'edificio':
        if sort == 'asc':
            salas = salas.order_by(order_by)
        else:
            sorter = '-' + order_by
            salas = salas.order_by(sorter)
    elif order_by == 'sala':
        if sort == 'asc':
            salas = salas.order_by('identificacao')
        else:
            salas = salas.order_by('-identificacao')
    #END order_by

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(salas, 8)
    try:
        salas = paginator.page(page)
    except PageNotAnInteger:
        salas = paginator.page(1)
    except EmptyPage:
        salas = paginator.page(paginator.num_pages)
    #END pagination

    return render(request, 'diaabertoapp/configurarespacos.html', {'utilizador':utilizador,'campus':campus, 'nomesquery':nome_query, 'campusquery':campus_query,'edificioquery':edificio_query, 'edificios':edificios, 'salas':salas, 'espacos':salas,'order_by':order_by, 'sort':sort})
#========================================================================================================================
#Configuracao das unidades organicas e departamentos
#Reedireciona para a pagina das configuracoes das unidades organicas e departamentos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurarorganicasdepartamentos(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    #BEGIN filter_by_organica
    organica_query = request.GET.get('organica')
    if organica_query !='' and organica_query is not None:
        departamentos = departamentos.filter(unidadeorganica=organica_query)
        organicas = organicas.filter(id=organica_query)
    #END filter_by_organica
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        departamentos = departamentos.filter(nome__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'organica':
        if sort == 'asc':
            departamentos = departamentos.order_by('unidadeorganica__nome')
        else:
            departamentos = departamentos.order_by('-unidadeorganica__nome')
    elif order_by == 'departamento':
        if sort == 'asc':
            departamentos = departamentos.order_by('nome')
        else:
            sorter = '-' + order_by
            departamentos = departamentos.order_by('-nome')
    #END order_by

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(departamentos, 8)
    try:
        departamentos = paginator.page(page)
    except PageNotAnInteger:
        departamentos = paginator.page(1)
    except EmptyPage:
        departamentos = paginator.page(paginator.num_pages)
    #END pagination
    
    return render(request, 'diaabertoapp/configurarorganicasdepartamentos.html', {'utilizador':utilizador,'nomesquery':nome_query, 'organicaquery':organica_query, 'organicas':organicas, 'departamentos':departamentos, 'order_by':order_by, 'sort':sort})

#========================================================================================================================
#Configuracao das unidades organicas
#Reedireciona para a pagina das configuracoes das unidades organicas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurarorganicas(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organicas = UnidadeOrganica.objects.all()

    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        organicas = organicas.filter(nome__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'unidadeorganica':
        if sort == 'asc':
            organicas = organicas.order_by('nome')
        else:
            organicas = organicas.order_by('-nome')
    #END order_by

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(organicas, 8)
    try:
        organicas = paginator.page(page)
    except PageNotAnInteger:
        organicas = paginator.page(1)
    except EmptyPage:
        organicas = paginator.page(paginator.num_pages)
    #END pagination
    return render(request, 'diaabertoapp/configurarorganicas.html', {'utilizador':utilizador,'nomesquery':nome_query,'organicas':organicas, 'order_by':order_by, 'sort':sort})
#========================================================================================================================
#Configuracao dos departamentos
#Reedireciona para a pagina das configuracoes dos departamentos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurardepartamentos(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    #BEGIN filter_by_organica
    organica_query = request.GET.get('organica')
    if organica_query !='' and organica_query is not None:
        departamentos = departamentos.filter(unidadeorganica=organica_query)
        organicas = organicas.filter(id=organica_query)
    #END filter_by_organica
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        departamentos = departamentos.filter(nome__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'unidadeorganica':
        if sort == 'asc':
            departamentos = departamentos.order_by('unidadeorganica')
        else:
            departamentos = departamentos.order_by('-unidadeorganica')
    elif order_by == 'departamento':
        if sort == 'asc':
            departamentos = departamentos.order_by('nome')
        else:
            departamentos = departamentos.order_by('-nome')

    #END order_by

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(departamentos, 8)
    try:
        departamentos = paginator.page(page)
    except PageNotAnInteger:
        departamentos = paginator.page(1)
    except EmptyPage:
        departamentos = paginator.page(paginator.num_pages)
    #END pagination
    print(organica_query)
    return render(request, 'diaabertoapp/configurardepartamentos.html', {'utilizador':utilizador,'nomesquery':nome_query,'organicas':organicas, 'departamentos':departamentos, 'organicaquery':organica_query, 'order_by':order_by, 'sort':sort})

#========================================================================================================================
#Configuracao dos campus
#Reedireciona para a pagina das configuracoes dos campus se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurarcampus(request):

    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        campus = campus.filter(nome__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'nome':
        if sort == 'asc':
            campus = campus.order_by('nome')
        else:
            campus = campus.order_by('-nome')
    elif order_by == 'morada':
        if sort == 'asc':
            campus = campus.order_by('morada')
        else:
            campus = campus.order_by('-morada')
    elif order_by == 'contacto':
        if sort == 'asc':
            campus = campus.order_by('contacto')
        else:
            campus = campus.order_by('-contacto')

    #END order_by
    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(campus, 12)
    try:
        campus = paginator.page(page)
    except PageNotAnInteger:
        campus = paginator.page(1)
    except EmptyPage:
        campus = paginator.page(paginator.num_pages)
    #END pagination
    return render(request, 'diaabertoapp/configurarcampus.html', {'utilizador':utilizador,'campus':campus,'order_by':order_by,'sort':sort,'nomesquery':nome_query})
#========================================================================================================================
#Configuracao dos edificios
#Reedireciona para a pagina das configuracoes dos edificios se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configuraredificios(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()

    #BEGIN filter_by_campus
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
        edificios = edificios.filter(campus=campus_query)
        campus = campus.filter(id=campus_query)
        
    #END filter_by_campus
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        edificios = edificios.filter(nome__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'campus':
        if sort == 'asc':
            edificios = edificios.order_by('campus__nome')
        else:
            edificios = edificios.order_by('-campus__nome')
    elif order_by == 'edificio':
        if sort == 'asc':
            edificios = edificios.order_by('nome')
        else:
            sorter = '-' + order_by
            edificios = edificios.order_by('-nome')
    #END order_by

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(edificios, 12)
    try:
        edificios = paginator.page(page)
    except PageNotAnInteger:
        edificios = paginator.page(1)
    except EmptyPage:
        edificios = paginator.page(paginator.num_pages)
    #END pagination

    return render(request, 'diaabertoapp/configuraredificios.html', {'utilizador':utilizador,'campus':campus,'edificios':edificios,'order_by':order_by, 'sort':sort,'nomesquery':nome_query, 'campusquery':campus_query})
#========================================================================================================================
#Configuracao das salas
#Reedireciona para a pagina das configuracoes das salas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def configurarsalas(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    #BEGIN filter_by_campus
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
        salas = salas.filter(edificio__campus=campus_query)
        campus = campus.filter(id=campus_query)
        edificios = edificios.filter(campus=campus_query)
    #END filter_by_campus
    #BEGIN filter_by_campus
    edificio_query = request.GET.get('edificio')
    if edificio_query !='' and edificio_query is not None:
        salas = salas.filter(edificio=edificio_query)
        edificios = edificios.filter(id=edificio_query)
    #END filter_by_campus
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        salas = salas.filter(identificacao__icontains=nome_query)
    #END filter_by_name 
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'campus':
        if sort == 'asc':
            salas = salas.order_by('edificio__campus__nome')
        else:
            salas = salas.order_by('-edificio__campus__nome')
    elif order_by == 'edificio':
        if sort == 'asc':
            salas = salas.order_by(order_by)
        else:
            sorter = '-' + order_by
            salas = salas.order_by(sorter)
    elif order_by == 'sala':
        if sort == 'asc':
            salas = salas.order_by('identificacao')
        else:
            salas = salas.order_by('-identificacao')
    #END order_by
    #tens que enviar ------->           'order_by':order_by, 'sort':sort
    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(salas, 12)
    try:
        salas = paginator.page(page)
    except PageNotAnInteger:
        salas = paginator.page(1)
    except EmptyPage:
        salas = paginator.page(paginator.num_pages)
    #END pagination

    return render(request, 'diaabertoapp/configurarsalas.html', {'utilizador':utilizador,'campus':campus,'nomesquery':nome_query, 'campusquery':campus_query,'edificioquery':edificio_query,'edificios':edificios, 'salas':salas, 'espacos':salas,'order_by':order_by, 'sort':sort})
#========================================================================================================================
#Editar os edificios
#Reedireciona para a pagina de editar os edificios se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def editaredificio(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    espaco = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        aForm = EdificioForm(request.POST, request.FILES, instance=espaco)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O edifício foi editado com sucesso!')
            return HttpResponseRedirect('/configurarespacos/edificios/')
        else:
            print(aForm.errors)
    else:

        aForm = EdificioForm(initial = {'campus': espaco.campus.id },instance=espaco)

    return render(request, 'diaabertoapp/editaredificio.html', {'utilizador':utilizador,'campus':campus,'edificios':edificios, 'form':aForm})
#========================================================================================================================
#Editar os campus
#Reedireciona para a pagina de editar os campus se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def editarcampus(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    espaco = get_object_or_404(Campus, pk=pk)
    if request.method == 'POST':
        aForm = CampusForm(request.POST, request.FILES, instance=espaco)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O campus foi editado com sucesso!')
            return HttpResponseRedirect('/configurarespacos/campus/')
        else:
            print(aForm.errors)
    else:

        aForm = CampusForm(instance=espaco)

    return render(request, 'diaabertoapp/editarcampus.html', {'utilizador':utilizador,'campus':campus, 'form':aForm})
#========================================================================================================================
#Eliminar os edificios
#Reedireciona para a pagina de eliminar os edificios se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def eliminaredificio(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    object = Edificio.objects.get(pk=pk)
    try:
        object.delete()
        messages.success(request, 'O edifício foi eliminado!')
    except ProtectedError:
        messages.error(request, 'O edifício não pode ser eliminado! Outras dependências impedem que elimine o edifício.')
    #messages.success(request, 'O edifício foi eliminado!')
    return HttpResponseRedirect('/configurarespacos/edificios/')
#========================================================================================================================
#Eliminar os campus
#Reedireciona para a pagina de eliminar os campus se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def eliminarcampus(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    object = Campus.objects.get(pk=pk)
    try:
        object.delete()
        messages.success(request, 'O campus foi eliminado!')
    except ProtectedError:
        messages.error(request, 'O campus não pode ser eliminado! Outras dependências impedem que elimine.')
    #messages.success(request, 'O edifício foi eliminado!')
    return HttpResponseRedirect('/configurarespacos/campus/')
#========================================================================================================================
#Editar as salas
#Reedireciona para a pagina de editar as salas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def editarsala(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    espaco = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        aForm = SalaForm(request.POST, request.FILES, instance=espaco)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O espaço foi editado com sucesso!')
            return HttpResponseRedirect('/configurarespacos/salas/')
        else:
            print(aForm.errors)
    else:

        aForm = SalaForm(initial = {'campus': espaco.edificio.campus.id },instance=espaco)

    return render(request, 'diaabertoapp/editarsala.html', {'utilizador':utilizador,'campus':campus,'edificios':edificios,'salas':salas, 'form':aForm})
#========================================================================================================================
#Eliminar as salas
#Reedireciona para a pagina de eliminar as salas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def eliminarsala(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    object = Sala.objects.get(pk=pk)
    try:
        object.delete()
        messages.success(request, 'O espaço foi eliminado!')
    except ProtectedError:
        messages.error(request, 'O espaço não pode ser eliminado! Outras dependências impedem que elimine o espaço.')
    #messages.success(request, 'O espaço foi eliminado!')
    return HttpResponseRedirect('/configurarespacos/salas/')
#========================================================================================================================
#Adicionar as salas
#Reedireciona para a pagina de adicionar as salas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def adicionarsala(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    if request.method == 'POST':
        aForm = SalaForm(request.POST, request.FILES)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O espaço foi adicionado!')
            return HttpResponseRedirect('/configurarespacos/salas/')
        else:
            print(aForm.errors)
    else:
        aForm = SalaForm()

    return render(request, 'diaabertoapp/adicionarsala.html', {'utilizador':utilizador,'campus':campus,'edificios':edificios,'salas':salas, 'form':aForm})
#========================================================================================================================
#Adicionar os edificios
#Reedireciona para a pagina de adiciionar os edificios se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def adicionaredificio(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    if request.method == 'POST':
        aForm = EdificioForm(request.POST, request.FILES)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O edifício foi adicionado!')
            return HttpResponseRedirect('/configurarespacos/edificios/')
        else:
            print(aForm.errors)
    else:
        aForm = EdificioForm()

    return render(request, 'diaabertoapp/adicionaredificio.html', {'utilizador':utilizador,'campus':campus,'edificios':edificios, 'form':aForm})
#========================================================================================================================
#Adicionar os campus
#Reedireciona para a pagina de adicionar os campus se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def adicionarcampus(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    campus = Campus.objects.all()
   
    if request.method == 'POST':
        aForm = CampusForm(request.POST, request.FILES)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O campus foi adicionado!')
            return HttpResponseRedirect('/configurarespacos/campus/')
        else:
            print(aForm.errors)
    else:
        aForm = CampusForm()

    return render(request, 'diaabertoapp/adicionarcampus.html', {'utilizador':utilizador,'campus':campus, 'form':aForm})
#========================================================================================================================
#Editar as unidades organicas
#Reedireciona para a pagina de editar as unidades organicas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def editarorganica(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organica = get_object_or_404(UnidadeOrganica, pk=pk)
    if request.method == 'POST':
        aForm = UnidadeOrganicaForm(request.POST, instance=organica)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'A unidade orgânica foi editada com sucesso!')
            return HttpResponseRedirect('/configurarorganicasdepartamentos/organicas/')
        else:
            print(aForm.errors)
    else:

        aForm = UnidadeOrganicaForm(instance=organica)

    return render(request, 'diaabertoapp/editarorganica.html', {'utilizador':utilizador,'organica':organica,'form':aForm})
#========================================================================================================================
#Eliminar as unidades organicas
#Reedireciona para a pagina de eliminar as unidades organicas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def eliminarorganica(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    object = UnidadeOrganica.objects.get(pk=pk)
    try:
        object.delete()
        messages.success(request, 'A unidade orgânica foi eliminada com sucesso!')
    except ProtectedError:
        messages.error(request, 'A unidade orgânica não pode ser eliminada! Outras dependências impedem que elimine a unidade orgânica.')
    #messages.success(request, 'A unidade orgânica foi eliminada com sucesso!')
    return HttpResponseRedirect('/configurarorganicasdepartamentos/organicas/')
#========================================================================================================================
#Adicionar as unidades organicas
#Reedireciona para a pagina de adicionar as unidades organicas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def adicionarorganica(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organica = UnidadeOrganica.objects.all()
    if request.method == 'POST':
        aForm = UnidadeOrganicaForm(request.POST)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'Unidade orgânica adicionada com sucesso!')
            return HttpResponseRedirect('/configurarorganicasdepartamentos/organicas/')
        else:
            print(aForm.errors)
    else:
        aForm = UnidadeOrganicaForm()

    return render(request, 'diaabertoapp/adicionarorganica.html', {'organica':organica, 'utilizador':utilizador, 'form':aForm})
#========================================================================================================================
#Editar os departamentos
#Reedireciona para a pagina de editar os departamentos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def editardepartamento(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        aForm = DepartamentoForm(request.POST, instance=departamento)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O departamento foi editado com sucesso!')
            return HttpResponseRedirect('/configurarorganicasdepartamentos/departamentos/')
        else:
            print(aForm.errors)
    else:

        aForm = DepartamentoForm(instance=departamento)

    return render(request, 'diaabertoapp/editardepartamento.html', {'utilizador':utilizador,'departamento':departamento,'form':aForm})
#========================================================================================================================
#Eliminar os departamentos
#Reedireciona para a pagina de eliminar os departamentos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def eliminardepartamento(request, pk):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    object = Departamento.objects.get(pk=pk)
    try:
        object.delete()
        messages.success(request, 'O departamento foi eliminado com sucesso!')
    except ProtectedError:
        messages.error(request, 'O departamento não pode ser eliminado! Outras dependências impedem que elimine o departamento.')
    #messages.success(request, 'O departamento foi eliminado com sucesso!')
    return HttpResponseRedirect('/configurarorganicasdepartamentos/departamentos/')
#========================================================================================================================
#Adicionar os departamentos
#Reedireciona para a pagina de adicionar os departamentos se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def adicionardepartamento(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    if request.method == 'POST':
        aForm = DepartamentoForm(request.POST)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O departamento foi adicionado com sucesso!')
            return HttpResponseRedirect('/configurarorganicasdepartamentos/departamentos/')
        else:
            print(aForm.errors)
    else:
        aForm = DepartamentoForm()

    return render(request, 'diaabertoapp/adicionardepartamento.html', {'utilizador':utilizador,'departamentos':departamentos, 'organicas':organicas,'form':aForm})
#========================================================================================================================
#Configuracao das sessoes
#Reedireciona para a pagina de configuracao das sessoes se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def sessoes(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    sessoes = Sessao.objects.all().order_by('hora')
    SessoesFormSet = modelformset_factory(Sessao, form=SessoesForm, fields=('hora',), can_delete=True, extra=0)

    if request.method == "POST":
        sessoesForm = SessoesFormSet(request.POST, queryset=sessoes, prefix="sa")
        if sessoesForm.is_valid():
            sessoesForm.save()
            messages.success(request, 'Sessões configuradas com sucesso!')
            return HttpResponseRedirect('/configuraratividades/')
        else:
            print(sessoesForm.errors)
    else:
        sessoesForm = SessoesFormSet(queryset=sessoes, prefix="sa")

    return render(request, 'diaabertoapp/sessoes.html', {'utilizador':utilizador, 'sessoes':sessoes,'form':sessoesForm})
#========================================================================================================================
#Configuracao do publico-alvo
#Reedireciona para a pagina de configuracao do publico-alvo se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def publicoalvo(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    publicos = PublicoAlvo.objects.all().order_by('nome')
    PublicoAlvoFormSet = modelformset_factory(PublicoAlvo, form=PublicoAlvoForm, fields=('nome',), can_delete=True, extra=0)

    if request.method == "POST":
        publicoAlvoForm = PublicoAlvoFormSet(request.POST, queryset=publicos, prefix="sa")
        if publicoAlvoForm.is_valid():
            publicoAlvoForm.save()
            messages.success(request, 'Publico-alvo configurado com sucesso!')
            return HttpResponseRedirect('/configuraratividades/')
        else:
            print(publicoAlvoForm.errors)
    else:
        publicoAlvoForm = PublicoAlvoFormSet(queryset=publicos, prefix="sa")

    return render(request, 'diaabertoapp/publicoalvo.html', {'utilizador':utilizador, 'publicos':publicos,'form':publicoAlvoForm})
#========================================================================================================================
#Configuracao das tematicas
#Reedireciona para a pagina de configuracao das tematicas se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def tematicas(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    tematicas = Tematica.objects.all().order_by('tema')
    TematicasFormSet = modelformset_factory(Tematica, form=TematicasForm, fields=('tema',), can_delete=True, extra=0)

    if request.method == "POST":
        tematicasForm = TematicasFormSet(request.POST, queryset=tematicas, prefix="sa")
        if tematicasForm.is_valid():
            tematicasForm.save()
            messages.success(request, 'Temáticas configuradas com sucesso!')
            return HttpResponseRedirect('/configuraratividades/')
        else:
            print(tematicasForm.errors)
    else:
        tematicasForm = TematicasFormSet(queryset=tematicas, prefix="sa")

    return render(request, 'diaabertoapp/tematicas.html', {'utilizador':utilizador,'tematicas':tematicas,'form':tematicasForm})
#========================================================================================================================
#Configuracao dos tipos de atividades
#Reedireciona para a pagina de configuracao dos tipos de atividades se o utilizador for do tipo administrador
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador
#========================================================================================================================
def tipoatividade(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    tipos = TipoAtividade.objects.all().order_by('tipo')
    TipoAtividadeFormSet = modelformset_factory(TipoAtividade, form=TipoAtividadeForm, fields=('tipo',), can_delete=True, extra=0)

    if request.method == "POST":
        tipoatividadeForm = TipoAtividadeFormSet(request.POST, queryset=tipos, prefix="sa")
        if tipoatividadeForm.is_valid():
            tipoatividadeForm.save()
            messages.success(request, 'Tipos de atividades configuradas com sucesso!')
            return HttpResponseRedirect('/configuraratividades/')
        else:
            print(tipoatividadeForm.errors)
    else:
        tipoatividadeForm = TipoAtividadeFormSet(queryset=tipos, prefix="sa")

    return render(request, 'diaabertoapp/tipoatividade.html', {'utilizador':utilizador,'tematicas':tipos,'form':tipoatividadeForm})
#========================================================================================================================
#Minhas atividades
#Reedireciona para a pagina das atividades se o utilizador for do tipo administrador, coordenador ou docente
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo administrador, coordenador ou docente
#========================================================================================================================
def minhasatividades(request):
    #minhasatividades = Atividade.objects.all()
    utilizador = ''
    notificacoes = Notificacao.objects.none()
    atividade_list = Atividade.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if utilizador.utilizadortipo.tipo == 'Docente':
                atividade_list = Atividade.objects.filter(responsavel=utilizador.id)
            elif utilizador.utilizadortipo.tipo == 'Coordenador':
                utilizador_organica = utilizador.unidadeorganica
                #utilizador_departamento = utilizador.departamento
                atividade_list = Atividade.objects.filter(unidadeorganica=utilizador_organica)
            elif utilizador.utilizadortipo.tipo == 'Administrador':
                atividade_list = Atividade.objects.all()
            else:
                messages.error(request, 'Não tem permissões para aceder à pagina!')
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!')
            return HttpResponseRedirect('/index/')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina! É necessário efetuar o login!')
        return HttpResponseRedirect('/login/')
    campus_arr = Campus.objects.all()
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    tematicas = Tematica.objects.all()
    materiais = MaterialQuantidade.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    sessoes = Sessao.objects.all()
    sessoesatividade = SessaoAtividade.objects.all()
    tipoatividade = TipoAtividade.objects.all()
    #start_date = date(2008, 8, 15)   # start date
    try:
        diaaberto = DiaAberto.objects.first() # diaaberto configurations
    except DiaAberto.DoesNotExist:
        diaaberto = None   
    if(diaaberto is not None):
        start_date = diaaberto.data_inicio
        end_date = diaaberto.data_fim   # end date

        delta = end_date - start_date       # as timedelta
        dias_arr = []
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dias_arr.append(day)
        dias = dias_arr
    else:
        dias = ""

    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'nome' or order_by == 'data' or order_by == 'responsavel' or order_by == 'validada':
        if sort == 'asc':
            atividade_list = atividade_list.order_by(order_by)
        else:
            sorter = '-' + order_by
            atividade_list = atividade_list.order_by(sorter)
    #END order_by
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        atividade_list = atividade_list.filter(nome__icontains=nome_query)
    #END filter_by_name      
    #BEGIN filter_by_campus
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
        atividade_list = atividade_list.filter(campus=campus_query)
        campus_arr = campus_arr.filter(id=campus_query)
    #END filter_by_campus
    #BEGIN filter_by_unidadeorganica
    organica_query = request.GET.get('unidadeorganica')
    if organica_query !='' and organica_query is not None:
        atividade_list = atividade_list.filter(unidadeorganica=organica_query)
        organicas = organicas.filter(id=organica_query)
        departamentos = departamentos.filter(unidadeorganica=organica_query)
    #END filter_by_unidadeorganica
    #BEGIN filter_by_departamento
    departamento_query = request.GET.get('departamento')
    if departamento_query !='' and departamento_query is not None:
        atividade_list = atividade_list.filter(departamento=departamento_query)
        departamentos = departamentos.filter(id=departamento_query)
    #END filter_by_departamento
    #BEGIN filter_by_tematica
    tematica_query = request.GET.get('tematica')
    if tematica_query !='' and tematica_query is not None:
        atividade_list = atividade_list.filter(tematicas=tematica_query)
        tematicas = tematicas.filter(id=tematica_query)
    #END filter_by_tematica
    #BEGIN filter_by_publicoalvo
    publico_query = request.GET.get('publico_alvo')
    if publico_query !='' and publico_query is not None:
        atividade_list = atividade_list.filter(publico_alvo=publico_query)
        publico_alvo = publico_alvo.filter(id=publico_query)
    #END filter_by_tematica
    #BEGIN filter_by_estado
    estado_query = request.GET.get('validada')
    if estado_query !='' and estado_query is not None:
        atividade_list = atividade_list.filter(validada__icontains=estado_query)
    #END filter_by_estado
    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        atividade_list = atividade_list.filter(tipo_atividade=tipo_query)
        tipoatividade = tipoatividade.filter(id=tipo_query)
    #END filter_by_tipo



    #BEGIN filter_by_dia
    unique_sesaoatividade_obj = []
    dia_query = request.GET.get('dias')
    if dia_query !='' and dia_query is not None:
        print(dia_query)
        atividades_sessions_id = sessoesatividade.filter(dia=dia_query)
        for x in atividades_sessions_id:
            unique_sesaoatividade_obj.append(x.atividade.id)

        atividade_list = atividade_list.filter(id__in=unique_sesaoatividade_obj)


        #dias = dias_arr
    #END filter_by_dia




    #BEGIN filter_by_sessao
    unique_sesaoatividade_obj = []
    sessao_query = request.GET.get('sessao')
    if sessao_query !='' and sessao_query is not None:
        if dia_query !='' and dia_query is not None:
            atividades_sessions_id = sessoesatividade.filter(dia=dia_query).filter(sessao=sessao_query)
            for x in atividades_sessions_id:
                unique_sesaoatividade_obj.append(x.atividade.id)
        else:

            atividades_sessions_id = sessoesatividade.filter(sessao=sessao_query)
            for x in atividades_sessions_id:
                unique_sesaoatividade_obj.append(x.atividade.id)

        atividade_list = atividade_list.filter(id__in=unique_sesaoatividade_obj)
        sessoes = sessoes.filter(id=sessao_query)
    #END filter_by_sessao




    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(atividade_list, 5)
    try:
        atividades = paginator.page(page)
    except PageNotAnInteger:
        atividades = paginator.page(1)
    except EmptyPage:
        atividades = paginator.page(paginator.num_pages)
    #END pagination
    #BEGIN tipo_utilizador and estados filter 
    unique_valida_obj = []
    unique_valida_str = []
    
    for x in atividade_list:
        if x.validada not in unique_valida_str:
            unique_valida_obj.append(x)
            unique_valida_str.append(x.validada)
    #END tipo_utilizador and estados filter filter
    count_notificacoes = 0 
    for x in notificacoes:
        if(x.visto == False):
            count_notificacoes = count_notificacoes + 1
    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/minhasatividades.html', {'sessoesatividade':sessoesatividade,'dias':dias, 'diaquery':dia_query,'sessoes':sessoes,'sessoesquery':sessao_query,'count_notificacoes':count_notificacoes,'notificacoes':notificacoes,'utilizador':utilizador,'user':request.user,'atividades':atividades,'order_by':order_by,'sort':sort,'campuss': campus_arr, 'campusquery':campus_query ,'organicas':organicas,'organicaquery':organica_query,'departamentos':departamentos,'departamentoquery':departamento_query,'tematicas':tematicas,'tematicaquery':tematica_query,'tipoatividade':tipoatividade,'tipo_query':tipo_query,'estados':unique_valida_obj, 'estadosquery':estado_query, 'nomesquery':nome_query, 'materiais':materiais, 'publicoalvo':publico_alvo, 'publicoquery':publico_query})
#========================================================================================================================
#Propor atividade
#Reedireciona para a pagina de propor atividade se o utilizador for do tipo docente
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo docente
#========================================================================================================================
def proporatividade(request):

    tipos_atividade = TipoAtividade.objects.all()
    temas_atividade = Tematica.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    campi = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    distinct_sessoes = Sessao.objects.values('hora').distinct().count()
    
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        organicas = UnidadeOrganica.objects.get(id=utilizador.unidadeorganica.id)
        departamentos = Departamento.objects.get(id=utilizador.departamento.id)
        if utilizador is None or utilizador.utilizadortipo.tipo != 'Docente':
            messages.error(request, 'Não tem permissões para aceder à pagina!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina! É necessário autentificar-se.')
        return HttpResponseRedirect('/index')

    mFormSet = inlineformset_factory(Atividade, MaterialQuantidade, MaterialQuantidadeForm, fields=('material','quantidade',), extra=0, can_delete=True)
    sFormSet = inlineformset_factory(Atividade, SessaoAtividade, SessaoAtividadeForm, fields=('dia','sessao','numero_colaboradores',), extra=1 , can_delete=True)


    if request.method == 'POST':
        #BEGIN FORMSET FORM
        aForm = AtividadeForm(request.POST,initial = {'unidadeorganica': utilizador.unidadeorganica.id,'departamento': utilizador.departamento.id })
        
        mForm = mFormSet(request.POST, prefix='mq')
        sForm = sFormSet(request.POST, prefix='sa')
        #mForm = MaterialFormSet(request.POST, prefix='mq')
        #sForm = SessaoFormSet(request.POST, prefix='sa')
        if aForm.is_valid() and mForm.is_valid() and sForm.is_valid():
            atividade = aForm.save(commit=False)
            if request.user.is_authenticated:
                user_email = request.user.email
                utilizador = Utilizador.objects.get(email=user_email)
                atividade.responsavel = utilizador
            atividade.save()
            aForm.save_m2m()
            for mFs in mForm:
                material = mFs.save(commit=False)
                if material.material is not None and mFs.cleaned_data.get('DELETE') is not True:
                    material.atividade = atividade
                    material.save()
            for sFs in sForm:
                sessao = sFs.save(commit=False)
                if sessao.dia is not None and sessao.sessao is not None and sessao.numero_colaboradores is not None and sFs.cleaned_data.get('DELETE') is not True:
                    sessao.atividade = atividade
                    sessao.n_alunos = atividade.limite_participantes
                    sessao.save()
            messages.success(request, 'Proposta de atividade criada com sucesso!')
            return HttpResponseRedirect('/minhasatividades/')
        else:
           print(aForm.errors)
           print(mForm.errors)
           print(sForm.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        aForm = AtividadeForm(initial = {'unidadeorganica': utilizador.unidadeorganica.id,'departamento': utilizador.departamento.id })
        #mForm = [MaterialQuantidadeForm(prefix=str(x), instance=MaterialQuantidade()) for x in range(0,1)]
        #sForm = [SessaoAtividadeForm(prefix=str(y),instance=SessaoAtividade()) for y in range(0,1)]
        #mForm = MaterialFormSet(prefix='mq')
        #sForm = SessaoFormSet(prefix='sa')
        mForm = mFormSet(prefix='mq')
        sForm = sFormSet(prefix='sa')
    return render(request, 'diaabertoapp/proporatividade.html', {'tipos':tipos_atividade, 'tematicas':temas_atividade, 'publicosalvo':publico_alvo, 'campi':campi, 'edificios':edificios, 'salas':salas, 'departamentos':departamentos, 'organicas':organicas, 'form':aForm, 'form2':mForm, 'form3':sForm})
#========================================================================================================================
#Alterar/Editar atividade
#Reedireciona para a pagina de alterar atividade se o utilizador for do tipo docente
#Reedireciona para a pagina inicial se o utilizador nao tiver permissoes do tipo docente
#========================================================================================================================
def alteraratividade(request,pk):


    atividade = get_object_or_404(Atividade, pk=pk)
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not atividade.responsavel.id == utilizador.id:
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    tipos_atividade = TipoAtividade.objects.all()
    temas_atividade = Tematica.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    campi = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    distinct_sessoes = Sessao.objects.values('hora').distinct().count()
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        organicas = UnidadeOrganica.objects.get(id=utilizador.unidadeorganica.id)
        departamentos = Departamento.objects.get(id=utilizador.departamento.id)

    #mFormSet = modelformset_factory(MaterialQuantidade, fields=('material','quantidade'))
    mFormSet = inlineformset_factory(Atividade, MaterialQuantidade, MaterialQuantidadeForm, fields=('material','quantidade',), extra=0  , can_delete=True)
    sFormSet = inlineformset_factory(Atividade, SessaoAtividade, SessaoAtividadeForm, fields=('dia','sessao','numero_colaboradores',), extra=0 , can_delete=True)

    mQueryset = MaterialQuantidade.objects.filter(atividade=atividade)
    sQueryset = SessaoAtividade.objects.filter(atividade=atividade)

    if request.method == "POST":
        aForm = AtividadeForm(request.POST, instance=atividade)

        #mForm = mFormSet(request.POST, queryset=mQueryset)
        mForm = mFormSet(request.POST, instance=atividade, prefix='mq')
        sForm = sFormSet(request.POST, instance=atividade, prefix='sa')

        if aForm.is_valid() and mForm.is_valid() and sForm.is_valid():
            atividade = aForm.save(commit=False)
            atividade.validada = 'PD'
            atividade.save()
            aForm.save_m2m()
            mForm.save()
            sForm.save()
            messages.success(request, 'Proposta de atividade editada com sucesso!')
            return HttpResponseRedirect('/minhasatividades/')
        else:
            print(mForm.errors)
            print(sForm.errors)
    else:
        aForm = AtividadeForm(instance=atividade)
        mForm = mFormSet(instance=atividade, prefix='mq')
        sForm = sFormSet(instance=atividade, prefix='sa')
    return render(request, 'diaabertoapp/alteraratividade.html', {'utilizador':utilizador,'tipos':tipos_atividade, 'tematicas':temas_atividade, 'publicosalvo':publico_alvo, 'campi':campi, 'edificios':edificios, 'salas':salas, 'departamentos':departamentos, 'organicas':organicas, 'form':aForm, 'form2':mForm, 'form3':sForm})
#========================================================================================================================
#Aceitar atividade
#Utilizador do tipo coordenador da mesma unidade organica do docente da atividade pode aceitar a atividade
#========================================================================================================================
def aceitaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not object.unidadeorganica == utilizador.unidadeorganica:
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    object.validada = 'VD'
    proposta = object.nome
    responsavel = object.responsavel
    object.save()

    notificacao_obj = Notificacao(assunto="Proposta aceite", conteudo="Proposta "+proposta+" aceite!", utilizador_recebe=responsavel, utilizador_envia=utilizador, prioridade=2)
    notificacao_obj.save()
    messages.success(request, 'Atividade foi aceite!')
    return HttpResponseRedirect('/minhasatividades/')
#========================================================================================================================
#Rejeitar atividade
#Utilizador do tipo coordenador da mesma unidade organica do docente da atividade pode rejeitar a atividade
#========================================================================================================================
def rejeitaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not object.unidadeorganica == utilizador.unidadeorganica:
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    
    object.validada = 'RJ'
    proposta = object.nome
    responsavel = object.responsavel
    object.save()
    notificacao_obj = Notificacao(assunto="Proposta rejeitada", conteudo="Proposta "+proposta+" rejeitada!", utilizador_recebe=responsavel, utilizador_envia=utilizador, prioridade=2)
    notificacao_obj.save()
    messages.success(request, 'Atividade foi rejeitada!')
    return HttpResponseRedirect('/minhasatividades/')
#========================================================================================================================
#Eliminar atividade
#O docente responsavel pela atividade pode eliminar a atividade
#========================================================================================================================
def eliminaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if not object.responsavel.id == utilizador.id:
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    
    object.delete()
    messages.success(request, 'Atividade foi eliminada!')
    return HttpResponseRedirect('/minhasatividades/')
#========================================================================================================================
#Visto (dar visto/lido nas notificacoes recebidas
#O utilizador que recebe a notificacao pode dar visto na notificacao
#========================================================================================================================
def visto(request,pk):
    object = Notificacao.objects.get(pk=pk)
    object.visto = True
    object.save()
    #messages.success(request, 'Notificação vista!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#========================================================================================================================
#Sugerir alteracao (na proposta de atividade)
#O coordenador pode sugerir alteracao ao docente responsavel pela atividade 
#========================================================================================================================
def sugeriralteracao(request,pk):
    atividade = Atividade.objects.get(pk=pk)
    utilizador = ''
    notificacoes = Notificacao.objects.none()
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if utilizador.utilizadortipo.tipo == 'Coordenador':
                utilizador_organica = utilizador.unidadeorganica
      
    materiais = MaterialQuantidade.objects.all()
    sessoesatividade = SessaoAtividade.objects.all()
    #messages.success(request, 'Notificação vista!')
    count_notificacoes = 0 
    for x in notificacoes:
        if(x.visto == False):
            count_notificacoes = count_notificacoes + 1

    proposta = atividade.nome
    responsavel = atividade.responsavel
    if request.method == 'GET':
        solicitacao = request.GET.get('alteracao')
        if solicitacao:
            notificacao_obj = Notificacao(assunto="Solicitação para alteração da proposta "+proposta, conteudo="Foi solicitado: "+solicitacao, utilizador_recebe=responsavel, utilizador_envia=utilizador, prioridade=2)
            notificacao_obj.save()
            messages.success(request, 'A solicitação foi enviada com sucesso!')
            return HttpResponseRedirect('/minhasatividades/')
        else:
            messages.error(request, 'A solicitação não foi enviada! Tente novamente.')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/minhasatividades/')

    return render(request, 'diaabertoapp/sugeriralteracao.html', {'count_notificacoes':count_notificacoes, 'notificacoes':notificacoes,'utilizador':utilizador,'user':request.user,'Atividade':atividade,'materiais':materiais,'sessoesatividade':sessoesatividade})

#========================================================================================================================
#Consulta das atividades (validadas)
#Reedireciona para a pagina da consulta das atividades
#========================================================================================================================

def consultaratividades(request):
    #minhasatividades = Atividade.objects.all()
    utilizador = ''
    notificacoes = Notificacao.objects.none()
    atividade_list = Atividade.objects.filter(validada='VD')
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if utilizador.utilizadortipo.tipo == 'Coordenador':
                utilizador_organica = utilizador.unidadeorganica
        else:
            atividade_list = Atividade.objects.filter(validada='VD')
    else:
        atividade_list = Atividade.objects.all()
    campus_arr = Campus.objects.all()
    organicas = UnidadeOrganica.objects.all()
    departamentos = Departamento.objects.all()
    tematicas = Tematica.objects.all()
    materiais = MaterialQuantidade.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    sessoes = Sessao.objects.all()
    sessoesatividade = SessaoAtividade.objects.all()
    tipoatividade = TipoAtividade.objects.all()
    try:
        diaaberto = DiaAberto.objects.first() # diaaberto configurations
    except DiaAberto.DoesNotExist:
        diaaberto = None   
    if(diaaberto is not None):
        start_date = diaaberto.data_inicio
        end_date = diaaberto.data_fim   # end date

        delta = end_date - start_date       # as timedelta
        dias_arr = []
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dias_arr.append(day)
        dias = dias_arr
    else:
        dias = ""
    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'nome':
        if sort == 'asc':
            atividade_list = atividade_list.order_by(order_by)
        else:
            sorter = '-' + order_by
            atividade_list = atividade_list.order_by(sorter)
    if order_by == 'tipo':
        if sort == 'asc':
            atividade_list = atividade_list.order_by('tipo_atividade__tipo')
        else:
            sorter = '-' + order_by
            atividade_list = atividade_list.order_by('-tipo_atividade__tipo')
    if order_by == 'organica':
        if sort == 'asc':
            atividade_list = atividade_list.order_by('unidadeorganica__nome')
        else:
            sorter = '-' + order_by
            atividade_list = atividade_list.order_by('-unidadeorganica__nome')
    if order_by == 'departamento':
        if sort == 'asc':
            atividade_list = atividade_list.order_by('departamento__nome')
        else:
            sorter = '-' + order_by
            atividade_list = atividade_list.order_by('-departamento__nome')
    #END order_by
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        atividade_list = atividade_list.filter(nome__icontains=nome_query)
    #END filter_by_name      
    #BEGIN filter_by_campus
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
        atividade_list = atividade_list.filter(campus=campus_query)
        campus_arr = campus_arr.filter(id=campus_query)
    #END filter_by_campus
    #BEGIN filter_by_unidadeorganica
    organica_query = request.GET.get('unidadeorganica')
    if organica_query !='' and organica_query is not None:
        atividade_list = atividade_list.filter(unidadeorganica=organica_query)
        organicas = organicas.filter(id=organica_query)
        departamentos = departamentos.filter(unidadeorganica=organica_query)
    #END filter_by_unidadeorganica
    #BEGIN filter_by_departamento
    departamento_query = request.GET.get('departamento')
    if departamento_query !='' and departamento_query is not None:
        atividade_list = atividade_list.filter(departamento=departamento_query)
        departamentos = departamentos.filter(id=departamento_query)
    #END filter_by_departamento
    #BEGIN filter_by_tematica
    tematica_query = request.GET.get('tematica')
    if tematica_query !='' and tematica_query is not None:
        atividade_list = atividade_list.filter(tematicas=tematica_query)
        tematicas = tematicas.filter(id=tematica_query)
    #END filter_by_tematica
    #BEGIN filter_by_publicoalvo
    publico_query = request.GET.get('publico_alvo')
    if publico_query !='' and publico_query is not None:
        atividade_list = atividade_list.filter(publico_alvo=publico_query)
        publico_alvo = publico_alvo.filter(id=publico_query)
    #END filter_by_tematica
    #BEGIN filter_by_estado
    estado_query = request.GET.get('validada')
    if estado_query !='' and estado_query is not None:
        atividade_list = atividade_list.filter(validada__icontains=estado_query)
    #END filter_by_estado
    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        atividade_list = atividade_list.filter(tipo_atividade=tipo_query)
        tipoatividade = tipoatividade.filter(id=tipo_query)
    #END filter_by_tipo
    #BEGIN filter_by_dia
    unique_sesaoatividade_obj = []
    dia_query = request.GET.get('dias')
    if dia_query !='' and dia_query is not None:
        print(dia_query)
        atividades_sessions_id = sessoesatividade.filter(dia=dia_query)
        for x in atividades_sessions_id:
            unique_sesaoatividade_obj.append(x.atividade.id)

        atividade_list = atividade_list.filter(id__in=unique_sesaoatividade_obj)


        #dias = dias_arr
    #END filter_by_dia




    #BEGIN filter_by_sessao
    unique_sesaoatividade_obj = []
    sessao_query = request.GET.get('sessao')
    if sessao_query !='' and sessao_query is not None:
        if dia_query !='' and dia_query is not None:
            atividades_sessions_id = sessoesatividade.filter(dia=dia_query).filter(sessao=sessao_query)
            for x in atividades_sessions_id:
                unique_sesaoatividade_obj.append(x.atividade.id)
        else:

            atividades_sessions_id = sessoesatividade.filter(sessao=sessao_query)
            for x in atividades_sessions_id:
                unique_sesaoatividade_obj.append(x.atividade.id)

        atividade_list = atividade_list.filter(id__in=unique_sesaoatividade_obj)
        sessoes = sessoes.filter(id=sessao_query)
    #END filter_by_sessao


    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(atividade_list, 5)
    try:
        atividades = paginator.page(page)
    except PageNotAnInteger:
        atividades = paginator.page(1)
    except EmptyPage:
        atividades = paginator.page(paginator.num_pages)
    #END pagination
    #BEGIN tipo_utilizador and estados filter 
    unique_valida_obj = []
    unique_valida_str = []
    
    for x in atividade_list:
        if x.validada not in unique_valida_str:
            unique_valida_obj.append(x)
            unique_valida_str.append(x.validada)
    #END tipo_utilizador and estados filter filter
    count_notificacoes = 0 
    for x in notificacoes:
        if(x.visto == False):
            count_notificacoes = count_notificacoes + 1
    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/atividades.html', {'dias':dias, 'diaquery':dia_query,'count_notificacoes':count_notificacoes, 'notificacoes':notificacoes,'utilizador':utilizador,'user':request.user,'atividades':atividades,'order_by':order_by,'sort':sort,'campuss': campus_arr, 'campusquery':campus_query ,'organicas':organicas,'organicaquery':organica_query,'departamentos':departamentos,'departamentoquery':departamento_query,'tematicas':tematicas,'tematicaquery':tematica_query,'tipoatividade':tipoatividade,'tipo_query':tipo_query,'estados':unique_valida_obj, 'estadosquery':estado_query, 'nomesquery':nome_query, 'materiais':materiais, 'publicoalvo':publico_alvo, 'publicoquery':publico_query, 'sessoes':sessoes, 'sessoesquery':sessao_query, 'sessoesatividade':sessoesatividade})











#========================================================================================================================
#Tarefas Nugas
#========================================================================================================================


def get_tarefas(request):
    tarefas_1 = Tarefa.objects.none()
    aut_utilizador = ''
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Colaborador':
                tarefas_1 = Tarefa.objects.filter(coolaborador=aut_utilizador.id)
            elif aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                utilizador_organica = aut_utilizador.unidadeorganica
                coordenadores = Utilizador.objects.filter(unidadeorganica=utilizador_organica)
                tarefas_1 = Tarefa.objects.filter(cordenador__in=coordenadores)
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                tarefas_1 = Tarefa.objects.all()
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')
    utilizador = Utilizador.objects.filter(utilizadortipo = 3).order_by("nome")

    aform = TarefaForm()


#BEGIN filter_by_name
    nome_colab_query = request.GET.get('nomeColaborador')
    if nome_colab_query !='' and nome_colab_query is not None:
        tarefas_1 = tarefas_1.filter(coolaborador__nome__icontains=nome_colab_query)
#END filter_by_name


#BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        tarefas_1 = tarefas_1.filter(nome__icontains=nome_query)
#END filter_by_name

#BEGIN tipo_utilizador and estados filter 
    unique_valida_obj = []
    unique_valida_str = []

    for x in tarefas_1:
        if x.tipo_tarefa not in unique_valida_str:
            unique_valida_obj.append(x)
            unique_valida_str.append(x.tipo_tarefa)
    #END tipo_utilizador and estados filter filter
        
    ##BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        tarefas_1 = tarefas_1.filter(tipo_tarefa=tipo_query)

    #END filter_by_tipo
    
    #BEGIN filter_by_campus
    campus_arr = Campus.objects.all()
    campus_query = request.GET.get('campus')
    if campus_query !='' and campus_query is not None:
       users = Utilizadores.object.filter()
       tarefas_1 = tarefas_1.filter(campus=campus_query)
       campus_arr = campus_arr.filter(id=campus_query)
    #END filter_by_campus
   # 
   # #BEGIN filter_by_UnidadeOrganica
   # UnidadeOrganica_query = request.GET.get('UnidadeOrganica')
   # if UnidadeOrganica_query !='' and UnidadeOrganica_query is not None:
   #     tarefas_1 = tarefas_1.filter(UnidadeOrganica=UnidadeOrganica_query)
   #     UnidadeOrganicas = UnidadeOrganicas.filter(id=UnidadeOrganica_query)
   #     departamentos = departamentos.filter(UnidadeOrganica=UnidadeOrganica_query)
   # #END filter_by_UnidadeOrganica
   # 
   # #BEGIN filter_by_departamento
   # departamento_query = request.GET.get('departamento')
   # if departamento_query !='' and departamento_query is not None:
   #     tarefas_1 = tarefas_1.filter(departamento=departamento_query)
   #     departamentos = departamentos.filter(id=departamento_query)
   # #END filter_by_departamento
    

    #BEGIN order_by
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'dia':
        if sort == 'asc':
            tarefas_1 = tarefas_1.order_by('dia')
        else:
            tarefas_1 = tarefas_1.order_by('-dia')
    elif order_by == 'horario':
        if sort == 'asc':
            tarefas_1 = tarefas_1.order_by('horario')
        else:
            tarefas_1 = tarefas_1.order_by('-horario')
    elif order_by == 'nome':
        if sort == 'asc':
            tarefas_1 = tarefas_1.order_by('nome')
        else:
            tarefas_1 = tarefas_1.order_by('-nome')
    elif order_by == 'tipo':
        if sort == 'asc':
            tarefas_1 = tarefas_1.order_by('tipo_tarefa')
        else:
            tarefas_1 = tarefas_1.order_by('-tipo_tarefa')
    elif order_by == 'estado':
        if sort == 'asc':
            tarefas_1 = tarefas_1.order_by('estado')
        else:
            tarefas_1 = tarefas_1.order_by('-estado')
    #END order_by
   
    
   
    

    
     #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(tarefas_1, 5)
    try:
        tarefas = paginator.page(page)
    except PageNotAnInteger:
        tarefas = paginator.page(1)
    except EmptyPage:
        tarefas = paginator.page(paginator.num_pages)
    #END pagination
    #,'campuss': campus_arr, 'campusquery':campus_query ,'UnidadeOrganicas':UnidadeOrganicas,'UnidadeOrganicaquery':UnidadeOrganica_query,'departamentos':departamentos,'departamentoquery':departamento_query,
    return render(request, 'diaabertoapp/tarefas.html',{'utilizador':aut_utilizador,'campuss': campus_arr, 'campusquery':campus_query,'form':aform,'tipo_query':tipo_query, 'tarefas': tarefas, 'utilizadores':utilizador,'tiposs':unique_valida_obj,'nomesquery':nome_query,'nomesColaboradorQuery':nome_colab_query,'order_by':order_by, 'sort':sort})

def add_tarefa(request):

    #tarefas_1 = Tarefa.objects.none()
    aut_utilizador = ''
    editable = False
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                editable = True
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                editable = True
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')

    atividades = Atividade.objects.all()
    salas = Sala.objects.all()
    
    
    if request.method == 'POST':
        aForm = TarefaForm(request.POST)
        if aForm.is_valid():
            tarefa = aForm.save(commit = False)
            tarefa.cordenador = aut_utilizador
            if(tarefa.tipo_tarefa == 'PE'):
                tarefa.duracao = 15
            if(tarefa.tipo_tarefa == 'AV'):
                tarefa.duracao = tarefa.atividade.duracao
            tarefa.save()
            aForm.save_m2m()

            return HttpResponseRedirect('/tarefas/')
        else:
            print(aForm.errors)
    else:
        aForm = TarefaForm()
     
    return render(request, 'diaabertoapp/adicionartarefa.html', {'form':aForm, 'atividades': atividades, 'salas':salas, 'utilizador':aut_utilizador})
    
def rem_tarefa(request ,pk):
    tarefas_1 = Tarefa.objects.all()
    aut_utilizador = ''
    editable = False
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                editable = True
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                editable = True
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':
       obj = Tarefa.objects.filter(pk=pk).delete()
       return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))    
    return render(request, 'diaabertoapp/tarefas.html', {'tarefas': tarefas})



def atribuir_tarefa(request,pk):
    
    aut_utilizador = ''
    editable = False
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                editable = True
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                editable = True
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')

    tarefas_1 = Tarefa.objects.all()
    colaboradorids = request.POST.getlist('colaborador_id')

    
    if(len(colaboradorids) != 0):

        tarefa_obj = Tarefa.objects.get(pk=pk)
        tarefa_obj.coolaborador.clear()
        tarefa_obj.coolaborador.add(*colaboradorids)
        tarefa_obj.estado = 'AT'
        tarefa_obj.save()         
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'diaabertoapp/tarefas.html', {'tarefas': tarefas_1})

    
def remove_colab(request,pk):
    aut_utilizador = ''
    editable = False
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                editable = True
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                editable = True
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')
    tarefa_obj = Tarefa.objects.get(pk=pk)
    tarefa_obj.coolaborador.clear()
    tarefa_obj.estado = 'PA'
    tarefa_obj.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

def edit_tarefa(request, pk):

    tarefa = get_object_or_404(Tarefa, pk=pk)
    aut_utilizador = ''
    editable = False
    #tarefas_1 = Tarefa.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        aut_utilizador = Utilizador.objects.get(email=user_email)
        if aut_utilizador is not None:
            if aut_utilizador.utilizadortipo.tipo == 'Coordenador':
                if tarefa.cordenador == aut_utilizador.id:
                    editable = True
                else:
                    messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                    return HttpResponseRedirect('/index/')
            elif aut_utilizador.utilizadortipo.tipo == 'Administrador':
                editable = True
            else:
                messages.error(request, "Não tem permissões para aceder a este conteúdo.")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "É necessário login.")
            return HttpResponseRedirect('/login/')
    else:
        messages.error(request, "Não está autentificado. Aguarde um pouco, se o erro persistir, contacte o suporte.")
        return HttpResponseRedirect('/login/')

    tipo_tarefa = {
        ('AV', 'Atividade'),
        ('PE' , 'Percurso'),
        ('OT', 'Outra'),
        }

    
    
    atividades = Atividade.objects.all()
    salas = Sala.objects.all()
    

    if request.method == "POST":
       
        aForm = TarefaForm(request.POST, instance=tarefa)
       #aForm = AtividadeForm(request.POST,initial = {'unidadeorganica': utilizador.unidadeorganica.id,'departamento': utilizador.departamento.id })
        
        if aForm.is_valid():
            tarefa = aForm.save(commit=False)
            tarefa.estado = 'PA'
            tarefa.save()
            aForm.save_m2m()
            
            messages.success(request, 'Tarefa editada com sucesso!')
            return HttpResponseRedirect('/tarefas/')
        else:
            print(aForm.errors)
    else:
        aForm = TarefaForm(instance=tarefa)
       
    return render(request, 'diaabertoapp/editTarefa.html', {'form':aForm,'atividades': atividades, 'salas':salas, 'tipo_tarefa':tipo_tarefa})


def grupos_switch(request):
    data = request.GET.get('data', None)
    horas = request.GET.get('horas',None)
    sala  = request.GET.get('sala',None)
    tarefa  = request.GET.get('tarefa',None)   

    print("--------------------------------------------------")
    inscricaoids = []
    if tarefa is None:
        horas = horas + ":00"
    print(horas)
    novashoras = datetime.strptime(horas, '%H:%M:%S').time()
    print(novashoras)
    outrashoras = timedelta(seconds = ((novashoras.hour*3600)+(novashoras.minute*60)+novashoras.second))
    print(outrashoras)
    sessaoatividades = SessaoAtividade.objects.filter(atividade__sala__id = sala, dia = data)
    print(sessaoatividades)
    for sessaoatividade in sessaoatividades:
        atividade = sessaoatividade.atividade
        print(atividade)
        hora_inicio = sessaoatividade.sessao.hora
        hora_inicio_final = timedelta(seconds = ((hora_inicio.hour*3600)+(hora_inicio.minute*60)+hora_inicio.second))
        print(hora_inicio_final)
        atividade_duracao = timedelta(seconds=(atividade.duracao*60))
        print(atividade_duracao)


        tarefa_inicio = outrashoras - atividade_duracao

        if tarefa_inicio == hora_inicio_final:
            inscricaoid =  SessaoAtividadeInscricao.objects.filter(sessaoAtividade__sessao__hora = str(tarefa_inicio) , sessaoAtividade__atividade__sala = sala, sessaoAtividade__dia = data).values_list('inscricao', flat=True).order_by('id')
            
            for inscricao in inscricaoid:
                inscricaoids.append(inscricao)
                grupos = Tarefa.objects.filter(grupo=inscricao,localizacao_grupo=sala, dia=data, horario=horas)
                print(grupos)
                for grupo in grupos:
                    print(grupo)
                    print(grupo.grupo)
                    grupinhos = grupo.grupo.all()
                    print(grupinhos)
                    for grupozinhos in grupinhos:
                        if grupozinhos.id == inscricao:
                            if tarefa != None:
                                tarefa1 = Tarefa.objects.get(id=tarefa)
                                if(grupo != tarefa1):
                                    print("entrei")
                                    inscricaoids.remove(inscricao)
                            else:
                                inscricaoids.remove(inscricao)


    #sessaoatividade = SessaoAtividade.objects.filter(sessao__hora = horas, atividade__sala__id = sala, dia = data)
    #print(sessaoatividade)
    #atividade = sessaoatividade.atividade
    #print(atividade)
    #atividade_duracao = datetime.timedelta(seconds=(atividade.duracao*60))
    #print(atividade_duracao)
    #x = datetime.timedelta(seconds = ((horas.hour*3600)+(horas.minute*60)+horas.second))
    #print(x)
    #tarefa_inicio = x - atividade_duracao
    #print(tarefa_inicio)
    #inscricaoid = SessaoAtividadeInscricao.objects.filter(sessaoAtividade__sessao__hora = tarefa_inicio , sessaoAtividade__atividade__sala = sala, sessaoAtividade__dia = data).values_list('inscricao', flat=True).order_by('id')
    
    dados = {
       'idinscricao' : list(inscricaoids)
     }

    return JsonResponse(dados)

def user_switch(request):
   
    

    userlist = []
    usernamelist = []
    colaboracaolist = []
    tarefa = Tarefa.objects.get(pk =request.GET.get('tarefa',None))
    tarefa_tipo = tarefa.tipo_tarefa
    utilizadores = Utilizador.objects.filter(utilizadortipo = 3).order_by("nome")
    #print(tarefa.duracao)
    #print(tarefa.horario)
    d = timedelta(seconds=(tarefa.duracao*60))
    tarefa_inicio = timedelta(seconds = ((tarefa.horario.hour*3600)+(tarefa.horario.minute*60)+tarefa.horario.second))
    tarefa_fim = d + tarefa_inicio
    data_tarefa = tarefa.dia

    if(tarefa.estado == 'PA'):

        
        for utilizador in utilizadores:
            colaboracoes = Colaboracao.objects.filter(colaborador = utilizador)
   
            if(len(colaboracoes) != 0):
                for colaboracao in colaboracoes:
                    data_colaboracao  = colaboracao.data_colaboracao 
                    
                    hora_inicio_colab = timedelta(seconds = ((colaboracao.hora_inicio_colab.hour*3600)+(colaboracao.hora_inicio_colab.minute*60)+(colaboracao.hora_inicio_colab.second)))
                    hora_fim_colab    = timedelta(seconds = ((colaboracao.hora_fim_colab.hour*3600)+(colaboracao.hora_fim_colab.minute*60)+(colaboracao.hora_fim_colab.second)))
                     

                    if(data_colaboracao == data_tarefa and hora_inicio_colab <= tarefa_inicio and hora_fim_colab >= tarefa_fim ):

                        tarefa_atribuida = Tarefa.objects.filter(coolaborador = utilizador.id)
                        if(len(tarefa_atribuida)!=0):

                            for task in tarefa_atribuida:
  
                                duracao_task = timedelta(seconds=(task.duracao*60))
                                task_inicio = timedelta(seconds = ((task.horario.hour*3600)+(task.horario.minute*60)+task.horario.second))
                                task_fim = duracao_task + task_inicio
                                data_task = task.dia


                                if(data_task == data_tarefa ):
                                    if(( tarefa_inicio < task_inicio and tarefa_fim <= tarefa_inicio ) or (tarefa_fim > task_fim and tarefa_inicio >= task_fim)):
                                        if((tarefa_tipo == 'AV' and colaboracao.sala_de_aula == 1) or (tarefa_tipo == 'PE' and colaboracao.percurso == 1) or (tarefa_tipo =='OT')):
                                            userlist.append(utilizador.id)
                                            usernamelist.append(utilizador.nome)
                                            colaboracaolist.append(colaboracao.id)
                                    else:
                                        break
                                else:
                                    if((tarefa_tipo == 'AV' and colaboracao.sala_de_aula == 1) or (tarefa_tipo == 'PE' and colaboracao.percurso == 1) or (tarefa_tipo =='OT')):
                                        userlist.append(utilizador.id)
                                        usernamelist.append(utilizador.nome)
                                        colaboracaolist.append(colaboracao.id)
                        else:
                            if((tarefa_tipo == 'AV' and colaboracao.sala_de_aula == 1) or (tarefa_tipo == 'PE' and colaboracao.percurso == 1) or (tarefa_tipo =='OT')):
                                userlist.append(utilizador.id)
                                usernamelist.append(utilizador.nome)
                                colaboracaolist.append(colaboracao.id)

        dados = {
            'usernamelist' : usernamelist,
            'userlist' : userlist,
            'colaboracao' : colaboracaolist
         }

    return JsonResponse(dados)

#========================================================================================================================
#Transporte Rui
#========================================================================================================================
def configurartransporte(request):

    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')
    transporte_list = Transporte.objects.all()
       
    #BEGIN filter_by_numero
    numero_query = request.GET.get('numero')
    if numero_query !='' and numero_query is not None:
        transporte_list = transporte_list.filter(numero=numero_query)
    #END filter_by_numero

    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        transporte_list = transporte_list.filter(tipo_transporte__icontains=tipo_query)
    #END filter_by_tipo

    #BEGIN filter_by_transporte
    capacidade_query = request.GET.get('capacidade')
    if capacidade_query !='' and capacidade_query is not None:
        transporte_list = transporte_list.filter(capacidade=capacidade_query)
    #END filter_by_tipo

        #ORDER
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'tipo':
        if sort == 'asc':
            transporte_list = transporte_list.order_by('tipo_transporte')
        else:
            transporte_list = transporte_list.order_by('-tipo_transporte')
    elif order_by == 'numero':
        if sort == 'asc':
            transporte_list = transporte_list.order_by('numero')
        else:
            transporte_list = transporte_list.order_by('-numero')
    elif order_by == 'capacidade':
        if sort == 'asc':
            transporte_list = transporte_list.order_by('capacidade')
        else:
            transporte_list = transporte_list.order_by('-capacidade')

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(transporte_list, 5)
    try:
        transportes = paginator.page(page)
    except PageNotAnInteger:
        transportes = paginator.page(1)
    except EmptyPage:
        transportes = paginator.page(paginator.num_pages)
    #END pagination

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/configurartransporte.html', {'transportes':transportes, 'numeroquery':numero_query, 'tipoquery':tipo_query, 'capacidadequery':capacidade_query, 'order_by':order_by, 'sort':sort})

def adicionartransporte(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = TransporteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configurarhorario/')
    else:
        form = TransporteForm()
    return render(request, 'diaabertoapp/proportransporte.html', {'form':form})

def editartransporte(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    transporte = Transporte.objects.get(pk=id)
    if request.method == 'POST':
        form=TransporteForm(request.POST, instance=transporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'O transporte foi editado com sucesso!')
            return HttpResponseRedirect('/configurartransporte/')
        else:
            print(form.errors)
    else:
        form = TransporteForm(instance=transporte)

    return render(request, 'diaabertoapp/proportransporte.html', {'form':form})

def eliminartransporte(request, id):
    object = Transporte.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/configurartransporte/')



def configurarpercurso(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    percursos_list = Percurso.objects.all()

    #BEGIN filter_by_origem
    origem_query = request.GET.get('origem')
    if origem_query !='' and origem_query is not None:
        percursos_list = percursos_list.filter(origem__icontains=origem_query)
    #END filter_by_origem

    #BEGIN filter_by_destino
    destino_query = request.GET.get('destino')
    if destino_query !='' and destino_query is not None:
        percursos_list = percursos_list.filter(destino__icontains=destino_query)
    #END filter_by_destino




    #ORDER
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'origem':
        if sort == 'asc':
            percursos_list = percursos_list.order_by('origem')
        else:
            percursos_list = percursos_list.order_by('-origem')
    elif order_by == 'destino':
        if sort == 'asc':
            percursos_list = percursos_list.order_by('destino')
        else:
            percursos_list = percursos_list.order_by('-destino')

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(percursos_list, 5)
    try:
        percursos = paginator.page(page)
    except PageNotAnInteger:
        percursos = paginator.page(1)
    except EmptyPage:
        percursos = paginator.page(paginator.num_pages)
    #END pagination

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/configurarpercurso.html', {'percursos':percursos, 'origemquery':origem_query, 'destinoquery':destino_query, 'order_by':order_by, 'sort':sort})

def adicionarpercurso(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = PercursoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configurarpercurso/')
    else:
        form = PercursoForm()
    return render(request, 'diaabertoapp/adicionarpercurso.html', {'form':form})

def editarpercurso(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    percurso = Percurso.objects.get(pk=id)
    if request.method == 'POST':
        form=PercursoForm(request.POST, instance=percurso)
        if form.is_valid():
            form.save()
            messages.success(request, 'O percurso foi editado com sucesso!')
            return HttpResponseRedirect('/configurarpercurso/')
        else:
            print(form.errors)
    else:
        form = PercursoForm(instance=percurso)

    return render(request, 'diaabertoapp/adicionarpercurso.html', {'form':form})

def eliminarpercurso(request, id):
    object = Percurso.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/configurarpercurso/')

def configurarhorario(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    horarios_list = Horario.objects.all()

    #BEGIN hora partida
    horachegada_query = request.GET.get('horachegada')
    if horachegada_query !='' and horachegada_query is not None:
        horarios_list = horarios_list.filter(hora_chegada__icontains=horachegada_query)
    #END hora partida

    #BEGIN hora chegada
    horapartida_query = request.GET.get('horapartida')
    if horapartida_query !='' and horapartida_query is not None:
        horarios_list = horarios_list.filter(hora_partida__icontains=horapartida_query)
    #END hora chegada

     #BEGIN data
    data_query = request.GET.get('data')
    if data_query !='' and data_query is not None:
        horarios_list = horarios_list.filter(data=data_query)
    #END data

    #ORDER
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'horachegada':
        if sort == 'asc':
            horarios_list = horarios_list.order_by('hora_chegada')
        else:
            horarios_list = horarios_list.order_by('-hora_chegada')
    elif order_by == 'horapartida':
        if sort == 'asc':
            horarios_list = horarios_list.order_by('hora_partida')
        else:
            horarios_list = horarios_list.order_by('-hora_partida')
    elif order_by == 'data':
        if sort == 'asc':
            horarios_list = horarios_list.order_by('data')
        else:
            horarios_list = horarios_list.order_by('-data')
    #ENDORDER

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(horarios_list, 5)
    try:
        horarios = paginator.page(page)
    except PageNotAnInteger:
        horarios = paginator.page(1)
    except EmptyPage:
        horarios = paginator.page(paginator.num_pages)
    #END pagination

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/configurarhorario.html', {'horarios':horarios, 'horachegadaquery':horachegada_query, 'horapartidaquery':horapartida_query, 'dataquery':data_query, 'order_by':order_by, 'sort':sort})

def adicionarhorario(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configurarhorario/')
    else:
        form = HorarioForm()
    return render(request, 'diaabertoapp/adicionarhorario.html', {'form':form})

def editarhorario(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    horario = Horario.objects.get(pk=id)
    if request.method == 'POST':
        form=HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'O horario foi editado com sucesso!')
            return HttpResponseRedirect('/configurarhorario/')
        else:
            print(form.errors)
    else:
        form = HorarioForm(instance=horario)

    return render(request, 'diaabertoapp/adicionarhorario.html', {'form':form})

def eliminarhorario(request, id):
    object = Horario.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/configurarhorario/')

def configurarprato(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    pratos_list = Prato.objects.all()

    #BEGIN filter_by_nome
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        pratos_list = pratos_list.filter(nome__icontains=nome_query)
    #END filter_by_nome

    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        pratos_list = pratos_list.filter(tipo__icontains=tipo_query)
    #END filter_by_tipo

    #BEGIN filter_by_sopa
    sopa_query = request.GET.get('sopa')
    if sopa_query !='' and sopa_query is not None:
        pratos_list = pratos_list.filter(sopa__icontains=sopa_query)
    #END filter_by_sopa

    #BEGIN filter_by_sobremesa
    sobremesa_query = request.GET.get('sobremesa')
    if sobremesa_query !='' and sobremesa_query is not None:
        pratos_list = pratos_list.filter(sobremesa__icontains=sobremesa_query)
    #END filter_by_sobremesa

    #ORDER
    order_by = request.GET.get('order_by')
    sort = request.GET.get('sort')
    if order_by == 'nome':
        if sort == 'asc':
            pratos_list = pratos_list.order_by('nome')
        else:
            pratos_list = pratos_list.order_by('-nome')
    elif order_by == 'tipo':
        if sort == 'asc':
            pratos_list = pratos_list.order_by('tipo')
        else:
            pratos_list = pratos_list.order_by('-tipo')
    elif order_by == 'sopa':
        if sort == 'asc':
            pratos_list = pratos_list.order_by('sopa')
        else:
            pratos_list = pratos_list.order_by('-sopa')
    elif order_by == 'sobremesa':
        if sort == 'asc':
            pratos_list = pratos_list.order_by('sobremesa')
        else:
            pratos_list = pratos_list.order_by('-sobremesa')

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(pratos_list, 5)
    try:
        pratos = paginator.page(page)
    except PageNotAnInteger:
        pratos = paginator.page(1)
    except EmptyPage:
        pratos = paginator.page(paginator.num_pages)
    #END pagination

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/configurarprato.html', {'pratos':pratos, 'order_by':order_by, 'sort':sort, 'nomequery':nome_query, 'sopaquery':sopa_query, 'sobremesaquery':sobremesa_query, 'tipoquery':tipo_query})

def adicionarprato(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = PratoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configurarprato/')
    else:
        form = PratoForm()
    return render(request, 'diaabertoapp/adicionarprato.html', {'form':form})

def editarprato(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    prato = Prato.objects.get(pk=id)
    if request.method == 'POST':
        form=PratoForm(request.POST, instance=prato)
        if form.is_valid():
            form.save()
            messages.success(request, 'O prato foi editado com sucesso!')
            return HttpResponseRedirect('/configurarprato/')
        else:
            print(form.errors)
    else:
        form = PratoForm(instance=prato)

    return render(request, 'diaabertoapp/adicionarprato.html', {'form':form})

def eliminarprato(request, id):
    object = Prato.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/configurarprato/')

def almocos(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    ementas_list = Ementa.objects.all()
    pratos_list = Prato.objects.all()


    #BEGIN filter_by_nome
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        pratos_list = pratos_list.filter(nome__icontains=nome_query)
        ementas_list = ementas_list.filter(prato__in=pratos_list)
    #END filter_by_nome

    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        pratos_list = pratos_list.filter(tipo__icontains=tipo_query)
        ementas_list = ementas_list.filter(prato__in=pratos_list)
    #END filter_by_tipo

    #BEGIN filter_by_sopa
    sopa_query = request.GET.get('sopa')
    if sopa_query !='' and sopa_query is not None:
        pratos_list = pratos_list.filter(sopa__icontains=sopa_query)
        ementas_list = ementas_list.filter(prato__in=pratos_list)
    #END filter_by_sopa

    #BEGIN filter_by_sobremesa
    sobremesa_query = request.GET.get('sobremesa')
    if sobremesa_query !='' and sobremesa_query is not None:
        pratos_list = pratos_list.filter(sobremesa__icontains=sobremesa_query)
        ementas_list = ementas_list.filter(prato__in=pratos_list)
    #END filter_by_sobremesa
    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(ementas_list, 5)
    try:
        ementas = paginator.page(page)
    except PageNotAnInteger:
        ementas = paginator.page(1)
    except EmptyPage:
        ementas = paginator.page(paginator.num_pages)
    #END pagination
    return render(request, 'diaabertoapp/almocos.html', {'ementas':ementas, 'nomequery':nome_query, 'sopaquery':sopa_query, 'sobremesaquery':sobremesa_query, 'tipoquery':tipo_query})


def editarementa(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    ementa = Ementa.objects.get(pk=id)
    if request.method == 'POST':
        form=EmentaForm(request.POST, instance=ementa)
        if form.is_valid():
            form.save()
            messages.success(request, 'O almoço foi editado com sucesso!')
            return HttpResponseRedirect('/almocos/')
        else:
            print(form.errors)
    else:
        form = EmentaForm(instance=ementa)

    return render(request, 'diaabertoapp/adicionarementa.html', {'form':form})

def eliminarementa(request, id):
    object = Ementa.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/almocos/')

def adicionarementa(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = EmentaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/almocos/')
    else:
        form = EmentaForm()
    return render(request, 'diaabertoapp/adicionarementa.html', {'form':form})

def transportes(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    transporte_list = TransporteUniversitarioHorario.objects.all()
    percurso_list = Percurso.objects.all()
    horarios_list = Horario.objects.all()
    transportes_list = Transporte.objects.all()

    #BEGIN filter_by_origem
    origem_query = request.GET.get('origem')
    if origem_query !='' and origem_query is not None:
        percurso_list = percurso_list.filter(origem__icontains=origem_query)
        transporte_list = transporte_list.filter(percurso__in=percurso_list)
    #END filter_by_origem 

    #BEGIN filter_by_destino
    destino_query = request.GET.get('destino')
    if destino_query !='' and destino_query is not None:
        percurso_list = percurso_list.filter(destino__icontains=destino_query)
        transporte_list = transporte_list.filter(percurso__in=percurso_list)
    #END filter_by_destino

   #BEGIN filter_by_numero
    numero_query = request.GET.get('numero')
    if numero_query !='' and numero_query is not None:
        transportes_list = transportes_list.filter(numero=numero_query)
        transporte_list = transporte_list.filter(transporte_universitario__in=transportes_list)
    #END filter_by_numero

    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        transportes_list = transportes_list.filter(tipo_transporte__icontains=tipo_query)
        transporte_list = transporte_list.filter(transporte_universitario__in=transportes_list)
    #END filter_by_tipo

    #BEGIN filter_by_transporte
    capacidade_query = request.GET.get('capacidade')
    if capacidade_query !='' and capacidade_query is not None:
        transportes_list = transportes_list.filter(capacidade=capacidade_query)
        transporte_list = transporte_list.filter(transporte_universitario__in=transportes_list)
    #END filter_by_tipo

    #BEGIN hora partida
    horachegada_query = request.GET.get('horachegada')
    if horachegada_query !='' and horachegada_query is not None:
        horarios_list = horarios_list.filter(hora_chegada__icontains=horachegada_query)
        transporte_list = transporte_list.filter(horario__in=horarios_list)
    #END hora partida

    #BEGIN hora chegada
    horapartida_query = request.GET.get('horapartida')
    if horapartida_query !='' and horapartida_query is not None:
        horarios_list = horarios_list.filter(hora_partida__icontains=horapartida_query)
        transporte_list = transporte_list.filter(horario__in=horarios_list)
    #END hora chegada

     #BEGIN data
    data_query = request.GET.get('data')
    if data_query !='' and data_query is not None:
        horarios_list = horarios_list.filter(data=data_query)
        transporte_list = transporte_list.filter(horario__in=horarios_list)
    #END data

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(transporte_list, 5)
    try:
        transportes = paginator.page(page)
    except PageNotAnInteger:
        transportes = paginator.page(1)
    except EmptyPage:
        transportes = paginator.page(paginator.num_pages)
    #END pagination

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/transportes.html', {'transportes':transportes, 'origemquery':origem_query, 'destinoquery':destino_query, 'numeroquery':numero_query, 'tipoquery':tipo_query, 'capacidadequery':capacidade_query, 'horachegadaquery':horachegada_query, 'horapartidaquery':horapartida_query, 'dataquery':data_query})



def adicionartransporteuniversitario(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = TransporteUniversitarioHorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/transportes/')
    else:
        form = TransporteUniversitarioHorarioForm()
    return render(request, 'diaabertoapp/adicionartransporteUniversitario.html', {'form':form})

def editartransporteuniversitario(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    transporteuniversitario = TransporteUniversitarioHorario.objects.get(pk=id)
    if request.method == 'POST':
        form=TransporteUniversitarioHorarioForm(request.POST, instance=transporteuniversitario)
        if form.is_valid():
            form.save()
            messages.success(request, 'O transporte Universitario foi editado com sucesso!')
            return HttpResponseRedirect('/transportes/')
        else:
            print(form.errors)
    else:
        form = TransporteUniversitarioHorarioForm(instance=transporteuniversitario)

    return render(request, 'diaabertoapp/adicionartransporteuniversitario.html', {'form':form})

def eliminartransporteuniversitario(request, id):
    object = TransporteUniversitarioHorario.objects.get(pk=id)
    object.delete()
    return HttpResponseRedirect('/transportes/')

def diaaberto(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    diaabertos_list = DiaAberto.objects.all()

    #BEGIN pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(diaabertos_list, 5)
    try:
        diaabertos = paginator.page(page)
    except PageNotAnInteger:
        diaabertos = paginator.page(1)
    except EmptyPage:
        diaabertos = paginator.page(paginator.num_pages)
    #END pagination
    return render(request, 'diaabertoapp/configurardiaaberto.html', {'diaabertos':diaabertos, 'diaabertos_list':diaabertos_list})

def adicionardiaaberto(request):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    if request.method == 'POST':
        form = DiaabertoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/configurardiaaberto/')
    else:
        form = DiaabertoForm()
    return render(request, 'diaabertoapp/adicionarconfigurardiaaberto.html', {'form':form})

def editardiaaberto(request, id):
    utilizador = ''
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            notificacoes = Notificacao.objects.filter(utilizador_recebe=utilizador.id).order_by('-hora')
            if not utilizador.utilizadortipo.tipo == 'Administrador':
                messages.error(request, 'Não tem permissões para aceder à pagina!!')
                return HttpResponseRedirect('/index')
        else:
            messages.error(request, 'Não tem permissões para aceder à pagina!!')
            return HttpResponseRedirect('/index')
    else:
        messages.error(request, 'Não tem permissões para aceder à pagina!!')
        return HttpResponseRedirect('/index')

    diaaberto = DiaAberto.objects.get(pk=id)
    if request.method == 'POST':
        form=DiaabertoForm(request.POST, instance=diaaberto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuraçao editada com sucesso!')
            return HttpResponseRedirect('/configurardiaaberto/')
        else:
            print(form.errors)
    else:
        form = DiaabertoForm(instance=diaaberto)

    return render(request, 'diaabertoapp/adicionarconfigurardiaaberto.html', {'form':form})
