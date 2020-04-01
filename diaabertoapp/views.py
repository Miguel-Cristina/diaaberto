from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Edificio, Atividade, Campus, Faculdade, Departamento, Tematica, PublicoAlvo, Sala, MaterialQuantidade, Sessao, SessaoAtividade
from .forms import CampusForm, AtividadeForm, MaterialQuantidadeForm, SessaoAtividadeForm, MaterialFormSet, SessaoFormSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def tarefas(request):
    return render(request, 'diaabertoapp/tarefas.html', {})



def minhasatividades(request):
    #minhasatividades = Atividade.objects.all()
    atividade_list = Atividade.objects.all()
    campus_arr = Campus.objects.all()
    faculdades = Faculdade.objects.all()
    departamentos = Departamento.objects.all()
    tematicas = Tematica.objects.all()
    materiais = MaterialQuantidade.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    sessoes = Sessao.objects.all()
    sessoesatividade = SessaoAtividade.objects.all()
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
        atividade_list = atividade_list.filter(tipo_atividade__icontains=tipo_query)
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
    unique_tipo_obj = []
    unique_tipo_str = []
    unique_valida_obj = []
    unique_valida_str = []
    
    for x in atividade_list:
        if x.tipo_atividade not in unique_tipo_str:
            unique_tipo_obj.append(x)
            unique_tipo_str.append(x.tipo_atividade)
        if x.validada not in unique_valida_str:
            unique_valida_obj.append(x)
            unique_valida_str.append(x.validada)
    #END tipo_utilizador and estados filter filter 

    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/minhasatividades.html', {'atividades':atividades,'campuss': campus_arr, 'campusquery':campus_query ,'faculdades':faculdades,'faculdadequery':faculdade_query,'departamentos':departamentos,'departamentoquery':departamento_query,'tematicas':tematicas,'tematicaquery':tematica_query,'tipoatividade':unique_tipo_obj,'tipo_query':tipo_query,'estados':unique_valida_obj, 'estadosquery':estado_query, 'nomesquery':nome_query, 'tiposatividades':unique_tipo_obj, 'materiais':materiais, 'publicoalvo':publico_alvo, 'publicoquery':publico_query, 'sessoes':sessoes, 'sessoesquery':sessao_query, 'sessoesatividade':sessoesatividade})

def proporatividade(request):
    def Sort_Tuple(tup):  
  
        # reverse = None (Sorts in Ascending order)  
        # key is set to sort using second element of  
        # sublist lambda has been used  
        return(sorted(tup, key = lambda x: x[1]))
    tipos_atividade = {('VI', 'Visitas Instalações'),
        ('VL' , 'Visitas Laboratórios'),
        ('AE' , 'Atividades Experimentais'),
	    ('AT' ,'Atividades Tecnológicas'),
	    ('FC' ,'Feira das Ciências'),
	    ('PL' ,'Palestras'),
	    ('CF' ,'Conferências'),
	    ('SM' ,'Seminários'),
	    ('TT' ,'Tertúlias'),
	    ('OE' ,'Outras Atividades (Ensino)'),
	    ('OC' ,'Outras Atividades (Culturais)'),
	    ('OD' ,'Outras Atividades (Desportivas)'),
	    ('EX' ,'Exposições'),
	    ('PS' ,'Passeios'),
	    ('OU' ,'Outras Atividades'),}
    temas_atividade = Tematica.objects.all()
    publico_alvo = PublicoAlvo.objects.all()
    tipos_ordered = Sort_Tuple(tipos_atividade)
    campi = Campus.objects.all()
    edificios = Edificio.objects.all()
    salas = Sala.objects.all()
    faculdades = Faculdade.objects.get(id=2)
    departamentos = Departamento.objects.get(id=1)
    distinct_sessoes = Sessao.objects.values('hora').distinct().count()

    if request.method == 'POST':
        # BEGIN INSTANCE FORM
   #     aForm = AtividadeForm(request.POST)
   #     mForm = [MaterialQuantidadeForm(request.POST, prefix=str(x), instance=MaterialQuantidade()) for x in range(0,1)]
   #     sForm = [SessaoAtividadeForm(request.POST, prefix=str(y), instance=SessaoAtividade()) for y in range(0,1)]
   #
   #     # check whether it's valid:
   #     if aForm.is_valid() and all([mf.is_valid() for mf in mForm]) and all([sf.is_valid() for sf in sForm]):
   #         atividade = aForm.save()
   #         for mFs in mForm:
   #             #if mFs.is_valid():
   #             #for mFs in mForm:
   #             material = mFs.save(commit=False)
   #             material.atividade = atividade
   #             material.save()
   #
   #         for sFs in sForm:
   #             #if sFs.is_valid():
   #             #for sFs in sForm:
   #             sessao = sFs.save(commit=False)
   #             sessao.atividade = atividade
   #             sessao.save()
        # END INSTANCE FORM
        #BEGIN FORMSET FORM
        aForm = AtividadeForm(request.POST)
        mForm = MaterialFormSet(request.POST)
        sForm = SessaoFormSet(request.POST)
        if aForm.is_valid() and mForm.is_valid() and sForm.is_valid():
            atividade = aForm.save()
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
            return HttpResponseRedirect('/minhasatividades/')
        else:
            aForm.errors
            mForm.errors
            sForm.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        aForm = AtividadeForm()
        #mForm = [MaterialQuantidadeForm(prefix=str(x), instance=MaterialQuantidade()) for x in range(0,1)]
        #sForm = [SessaoAtividadeForm(prefix=str(y),instance=SessaoAtividade()) for y in range(0,1)]
        mForm = MaterialFormSet()
        sForm = SessaoFormSet()

    return render(request, 'diaabertoapp/proporatividade.html', {'tipos':tipos_ordered, 'tematicas':temas_atividade, 'publicosalvo':publico_alvo, 'campi':campi, 'edificios':edificios, 'salas':salas, 'departamentos':departamentos, 'faculdades':faculdades, 'form':aForm, 'form2':mForm, 'form3':sForm})

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