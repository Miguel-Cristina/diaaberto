from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404 
from django.db.models import Count
from .models import Edificio, Atividade, Campus, Faculdade, Departamento, Tematica, TipoAtividade,Tarefa, PublicoAlvo, Sala, MaterialQuantidade, Sessao, SessaoAtividade, Utilizador, UtilizadorTipo, UtilizadorParticipante
from .forms import CampusForm, AtividadeForm, MaterialQuantidadeForm ,SessaoAtividadeForm, MaterialFormSet, TarefaForm, SessoesForm, SessaoFormSet, PublicoAlvoForm, TematicasForm, TipoAtividadeForm, CampusForm, EdificioForm, SalaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


 #Create your views here.
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/minhasatividades')
            else:
                messages.error(request, "Email ou password inválidos.")
        else:
            print(form.errors.as_text)
            messages.error(request, "Email ou password inválidos.")
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = "input"
    form.fields['password'].widget.attrs['class'] = "input"
    return render(request, 'diaabertoapp/login.html', {"form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "Sessão terminada. Até breve!")
    return redirect('/login')

def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def administrador(request):
    return render(request, 'diaabertoapp/administrador.html', {})

def configuraratividades(request):
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

    return render(request, 'diaabertoapp/configuraratividades.html', {'sessoes':sessoes, 'temas':temas, 'tipos':tipos, 'publicos':publicos,'order_by':order_by, 'sort':sort})

def configurarespacos(request):
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
    
    return render(request, 'diaabertoapp/configurarespacos.html', {'campus':campus, 'nomesquery':nome_query, 'campusquery':campus_query,'edificioquery':edificio_query, 'edificios':edificios, 'salas':salas, 'espacos':salas,'order_by':order_by, 'sort':sort})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def configurarcampus(request):
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    CampusFormSet = modelformset_factory(Campus, form=CampusForm, fields=('nome',), can_delete=True, extra=0)
    EdificiosFormSet = modelformset_factory(Edificio, form=EdificioForm, fields=('campus','nome',), can_delete=True, extra=0)
    #SessoesFormSet = modelformset_factory(Sessao, form=SessoesForm, fields=('hora',), can_delete=True, extra=0)

    if request.method == "POST":
        campusForm = CampusFormSet(request.POST, queryset=campus, prefix="sa")
        if campusForm.is_valid():
            campusForm.save()
            messages.success(request, 'Campus configuradas com sucesso!')
            return HttpResponseRedirect('/administrador/configurarespacos')
        else:
            print(campusForm.errors)
    else:
        campusForm = CampusFormSet(queryset=campus, prefix="sa")
        edificioForm = EdificiosFormSet(queryset=edificios, prefix="mq")

    return render(request, 'diaabertoapp/configurarcampus.html', {'campus':campus,'edificios':edificios,'salas':salas,'form':campusForm, 'form2':edificioForm})

def configuraredificios(request):
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    EdificiosFormSet = modelformset_factory(Edificio, form=EdificioForm, fields=('campus','nome',), can_delete=True, extra=0)
    #SessoesFormSet = modelformset_factory(Sessao, form=SessoesForm, fields=('hora',), can_delete=True, extra=0)

    if request.method == "POST":
        edificiosForm = EdificiosFormSet(request.POST, queryset=edificios, prefix="mq")
        if edificiosForm.is_valid():
            edificiosForm.save()
            messages.success(request, 'Edificios configurados com sucesso!')
            return HttpResponseRedirect('/administrador/configurarespacos')
        else:
            print(edificiosForm.errors)
    else:
        edificiosForm = EdificiosFormSet(queryset=edificios, prefix="mq")

    return render(request, 'diaabertoapp/configuraredificios.html', {'campus':campus,'edificios':edificios,'salas':salas,'form':edificiosForm})

def configurarsalas(request):
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
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
    paginator = Paginator(salas, 12)
    try:
        salas = paginator.page(page)
    except PageNotAnInteger:
        salas = paginator.page(1)
    except EmptyPage:
        salas = paginator.page(paginator.num_pages)
    #END pagination

    return render(request, 'diaabertoapp/configurarsalas.html', {'campus':campus,'edificios':edificios, 'salas':salas, 'espacos':salas,'order_by':order_by, 'sort':sort})

def editarsala(request, pk):
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    espaco = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        aForm = SalaForm(request.POST, instance=espaco)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O espaço foi editado com sucesso!')
            return HttpResponseRedirect('/administrador/configurarespacos/salas')
        else:
            print(aForm.errors)
    else:

        aForm = SalaForm(initial = {'campus': espaco.edificio.campus.id },instance=espaco)

    return render(request, 'diaabertoapp/adicionarsala.html', {'campus':campus,'edificios':edificios,'salas':salas, 'form':aForm})

def eliminarsala(request, pk):
    object = Sala.objects.get(pk=pk)
    object.delete()
    messages.success(request, 'O espaço foi eliminado!')
    return HttpResponseRedirect('/administrador/configurarespacos/salas')

def adicionarsala(request):
    campus = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    if request.method == 'POST':
        aForm = SalaForm(request.POST)
        if aForm.is_valid():
            aForm.save()
            messages.success(request, 'O espaço foi adicionado!')
            return HttpResponseRedirect('/administrador/configurarespacos/salas')
        else:
            print(aForm.errors)
    else:
        aForm = SalaForm()

    return render(request, 'diaabertoapp/adicionarsala.html', {'campus':campus,'edificios':edificios,'salas':salas, 'form':aForm})

def sessoes(request):
    sessoes = Sessao.objects.all().order_by('hora')
    SessoesFormSet = modelformset_factory(Sessao, form=SessoesForm, fields=('hora',), can_delete=True, extra=0)

    if request.method == "POST":
        sessoesForm = SessoesFormSet(request.POST, queryset=sessoes, prefix="sa")
        if sessoesForm.is_valid():
            sessoesForm.save()
            messages.success(request, 'Sessões configuradas com sucesso!')
            return HttpResponseRedirect('/administrador/configuraratividades')
        else:
            print(sessoesForm.errors)
    else:
        sessoesForm = SessoesFormSet(queryset=sessoes, prefix="sa")

    return render(request, 'diaabertoapp/sessoes.html', {'sessoes':sessoes,'form':sessoesForm})

def publicoalvo(request):
    publicos = PublicoAlvo.objects.all().order_by('nome')
    PublicoAlvoFormSet = modelformset_factory(PublicoAlvo, form=PublicoAlvoForm, fields=('nome',), can_delete=True, extra=0)

    if request.method == "POST":
        publicoAlvoForm = PublicoAlvoFormSet(request.POST, queryset=publicos, prefix="sa")
        if publicoAlvoForm.is_valid():
            publicoAlvoForm.save()
            messages.success(request, 'Publico-alvo configurado com sucesso!')
            return HttpResponseRedirect('/administrador/configuraratividades')
        else:
            print(publicoAlvoForm.errors)
    else:
        publicoAlvoForm = PublicoAlvoFormSet(queryset=publicos, prefix="sa")

    return render(request, 'diaabertoapp/publicoalvo.html', {'publicos':publicos,'form':publicoAlvoForm})

def tematicas(request):
    tematicas = Tematica.objects.all().order_by('tema')
    TematicasFormSet = modelformset_factory(Tematica, form=TematicasForm, fields=('tema',), can_delete=True, extra=0)

    if request.method == "POST":
        tematicasForm = TematicasFormSet(request.POST, queryset=tematicas, prefix="sa")
        if tematicasForm.is_valid():
            tematicasForm.save()
            messages.success(request, 'Temáticas configuradas com sucesso!')
            return HttpResponseRedirect('/administrador/configuraratividades')
        else:
            print(tematicasForm.errors)
    else:
        tematicasForm = TematicasFormSet(queryset=tematicas, prefix="sa")

    return render(request, 'diaabertoapp/tematicas.html', {'tematicas':tematicas,'form':tematicasForm})

def tipoatividade(request):
    tipos = TipoAtividade.objects.all().order_by('tipo')
    TipoAtividadeFormSet = modelformset_factory(TipoAtividade, form=TipoAtividadeForm, fields=('tipo',), can_delete=True, extra=0)

    if request.method == "POST":
        tipoatividadeForm = TipoAtividadeFormSet(request.POST, queryset=tipos, prefix="sa")
        if tipoatividadeForm.is_valid():
            tipoatividadeForm.save()
            messages.success(request, 'Tipos de atividades configuradas com sucesso!')
            return HttpResponseRedirect('/administrador/configuraratividades')
        else:
            print(tipoatividadeForm.errors)
    else:
        tipoatividadeForm = TipoAtividadeFormSet(queryset=tipos, prefix="sa")

    return render(request, 'diaabertoapp/tipoatividade.html', {'tematicas':tipos,'form':tipoatividadeForm})

def minhasatividades(request):
    #minhasatividades = Atividade.objects.all()
    utilizador = ''
    atividade_list = Atividade.objects.all()
    if request.user.is_authenticated:
        user_email = request.user.email
        utilizador = Utilizador.objects.get(email=user_email)
        if utilizador is not None:
            if utilizador.utilizadortipo_id == 2:
                atividade_list = Atividade.objects.filter(responsavel=utilizador.id)
            elif utilizador.utilizadortipo_id == 4:
                utilizador_faculdade = utilizador.faculdade
                utilizador_departamento = utilizador.departamento
                atividade_list = Atividade.objects.filter(faculdade=utilizador_faculdade, departamento=utilizador_departamento)
        else:
            atividade_list = Atividade.objects.all()
    else:
        atividade_list = Atividade.objects.all()
    campus_arr = Campus.objects.all()
    faculdades = Faculdade.objects.all()
    departamentos = Departamento.objects.all()
    tematicas = Tematica.objects.all()
    materiais = MaterialQuantidade.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    sessoes = Sessao.objects.all()
    sessoesatividade = SessaoAtividade.objects.all()
    tipoatividade = TipoAtividade.objects.all()

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
    #BEGIN filter_by_faculdade
    faculdade_query = request.GET.get('faculdade')
    if faculdade_query !='' and faculdade_query is not None:
        atividade_list = atividade_list.filter(faculdade=faculdade_query)
        faculdades = faculdades.filter(id=faculdade_query)
        departamentos = departamentos.filter(faculdade=faculdade_query)
    #END filter_by_faculdade
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
    #BEGIN filter_by_sessao
    unique_sesaoatividade_obj = []
    sessao_query = request.GET.get('sessao')
    if sessao_query !='' and sessao_query is not None:
        atividades_sessions_id = sessoesatividade.filter(sessao=sessao_query)
        for x in atividades_sessions_id:
            unique_sesaoatividade_obj.append(x.atividade)
        atividade_list = unique_sesaoatividade_obj
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

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/minhasatividades.html', {'utilizador':utilizador,'user':request.user,'atividades':atividades,'order_by':order_by,'sort':sort,'campuss': campus_arr, 'campusquery':campus_query ,'faculdades':faculdades,'faculdadequery':faculdade_query,'departamentos':departamentos,'departamentoquery':departamento_query,'tematicas':tematicas,'tematicaquery':tematica_query,'tipoatividade':tipoatividade,'tipo_query':tipo_query,'estados':unique_valida_obj, 'estadosquery':estado_query, 'nomesquery':nome_query, 'materiais':materiais, 'publicoalvo':publico_alvo, 'publicoquery':publico_query, 'sessoes':sessoes, 'sessoesquery':sessao_query, 'sessoesatividade':sessoesatividade})

def proporatividade(request):

    tipos_atividade = TipoAtividade.objects.all()
    temas_atividade = Tematica.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    campi = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    faculdades = Faculdade.objects.get(id=2)
    departamentos = Departamento.objects.get(id=1)
    distinct_sessoes = Sessao.objects.values('hora').distinct().count()

    if request.method == 'POST':
        #BEGIN FORMSET FORM
        aForm = AtividadeForm(request.POST)
        mForm = MaterialFormSet(request.POST, prefix='mq')
        sForm = SessaoFormSet(request.POST, prefix='sa')
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
                if material.material is not None:
                    material.atividade = atividade
                    material.save()
            for sFs in sForm:
                sessao = sFs.save(commit=False)
                if sessao.dia is not None and sessao.sessao is not None and sessao.numero_colaboradores is not None:
                    sessao.atividade = atividade
                    sessao.save()
            messages.success(request, 'Proposta de atividade criada com sucesso!')
            return HttpResponseRedirect('/minhasatividades/')
        else:
           print(aForm.errors)
           print(mForm.errors)
           print(sForm.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        aForm = AtividadeForm()
        #mForm = [MaterialQuantidadeForm(prefix=str(x), instance=MaterialQuantidade()) for x in range(0,1)]
        #sForm = [SessaoAtividadeForm(prefix=str(y),instance=SessaoAtividade()) for y in range(0,1)]
        mForm = MaterialFormSet(prefix='mq')
        sForm = SessaoFormSet(prefix='sa')
    return render(request, 'diaabertoapp/proporatividade.html', {'tipos':tipos_atividade, 'tematicas':temas_atividade, 'publicosalvo':publico_alvo, 'campi':campi, 'edificios':edificios, 'salas':salas, 'departamentos':departamentos, 'faculdades':faculdades, 'form':aForm, 'form2':mForm, 'form3':sForm})

def alteraratividade(request,pk):

    tipos_atividade = TipoAtividade.objects.all()
    temas_atividade = Tematica.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    campi = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    faculdades = Faculdade.objects.get(id=2)
    departamentos = Departamento.objects.get(id=1)
    distinct_sessoes = Sessao.objects.values('hora').distinct().count()

    atividade = get_object_or_404(Atividade, pk=pk)

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
    return render(request, 'diaabertoapp/alteraratividade.html', {'tipos':tipos_atividade, 'tematicas':temas_atividade, 'publicosalvo':publico_alvo, 'campi':campi, 'edificios':edificios, 'salas':salas, 'departamentos':departamentos, 'faculdades':faculdades, 'form':aForm, 'form2':mForm, 'form3':sForm})

def aceitaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    object.validada = 'VD'
    object.save()
    messages.success(request, 'Atividade foi aceite!')
    return HttpResponseRedirect('/minhasatividades/')

def rejeitaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    object.validada = 'RJ'
    object.save()
    messages.success(request, 'Atividade foi rejeitada!')
    return HttpResponseRedirect('/minhasatividades/')

def eliminaratividade(request,pk):
    object = Atividade.objects.get(pk=pk)
    object.delete()
    messages.success(request, 'Atividade foi eliminada!')
    return HttpResponseRedirect('/minhasatividades/')


def get_atividade(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateAtividade(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateAtividade()

    return render(request, 'proporatividade.html', {'form': form})


def edificios(request):
    edificios = Edificio.objects.all()
    return render(request, 'diaabertoapp/edificios.html', {'edificios':edificios})

def get_campus(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CampusForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            messages.success(request, 'The form is valid.')
        else:
            messages.error(request, 'The form is invalid.')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/admin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CampusForm()

    return render(request, 'proporatividade.html', {'form': form})


def get_edificios(request, campus_id):
    campus = Campus.objects.get(pk=campus_id)
    edificios = Edificio.objects.filter(campus=campus)
    edificio_dict = {}
    for edificio in edificios:
        edificio_dict[edificio.id] = edificio.nome
    return HttpResponse(json.dumps(edificio_dict), mimetype="application/json")

def get_salas(request, edificio_id):
    edificio = Edificio.objects.get(pk=edificio_id)
    salas = Sala.objects.filter(edificio=edificio)
    sala_dict = {}
    for sala in salas:
        sala_dict[sala.id] = sala.identificacao
    return HttpResponse(json.dumps(sala_dict), mimetype="application/json")

def get_tarefas(request):
    tarefas_1 = Tarefa.objects.all()
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

    return render(request, 'diaabertoapp/tarefas.html', {'tarefas': tarefas})

def add_tarefa(request):
    if request.method == 'POST':
        aForm = TarefaForm(request.POST)
        if aForm.is_valid():
            tarefa = aForm.save()
            return HttpResponseRedirect('/tarefas/')
        else:
            aForm.errors
    else:
        aForm = TarefaForm()
     
    return render(request, 'diaabertoapp/adicionartarefa.html', {'form':aForm, 'atividades': atividades})
    
def rem_tarefa(request ,pk):
    tarefas_1 = Tarefa.objects.all()
    
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
    print("entrei")
    if request.method == 'POST':
       obj = Tarefa.objects.filter(pk=pk).delete()
       return HttpResponseRedirect('/tarefas/')    
    return render(request, 'diaabertoapp/tarefas.html', {'tarefas': tarefas})