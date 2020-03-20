from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Count
from .models import Edificio, Atividade, Campus, Faculdade, Departamento, Tematica
from .forms import CampusForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def minhasatividades(request):
    #minhasatividades = Atividade.objects.all()
    atividade_list = Atividade.objects.all()
    campus_arr = Campus.objects.all()
    faculdades = Faculdade.objects.all()
    departamentos = Departamento.objects.all()
    tematicas = Tematica.objects.all()
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
    #
        
    #'tiposquery':tipo_query
    return render(request, 'diaabertoapp/minhasatividades.html', {'atividades':atividades, 'campuss': campus_arr, 'campusquery':campus_query ,'faculdades':faculdades,'faculdadequery':faculdade_query,'departamentos':departamentos,'departamentoquery':departamento_query,'tematicas':tematicas,'tematicaquery':tematica_query,'estados':unique_valida_obj, 'nomesquery':nome_query, 'tiposatividades':unique_tipo_obj, 'estadosquery':estado_query})

def proporatividade(request):
    return render(request, 'diaabertoapp/proporatividade.html', {})


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