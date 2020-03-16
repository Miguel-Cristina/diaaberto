from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Count
from .models import Edificio, Atividade
from .forms import CampusForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def minhasatividades(request):
    #minhasatividades = Atividade.objects.all()
    atividade_list = Atividade.objects.all()
    #BEGIN filter_by_name
    nome_query = request.GET.get('nome')
    if nome_query !='' and nome_query is not None:
        atividade_list = atividade_list.filter(nome__icontains=nome_query)
    #END filter_by_name
    #BEGIN filter_by_tipo
    tipo_query = request.GET.get('tipo')
    if tipo_query !='' and tipo_query is not None:
        atividade_list = atividade_list.filter(tipo_atividade__icontains=tipo_query)
    #END filter_by_tipo
        #BEGIN filter_by_tipo
    estado_query = request.GET.get('validada')
    if estado_query !='' and estado_query is not None:
        atividade_list = atividade_list.filter(validada__icontains=estado_query)
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

    return render(request, 'diaabertoapp/minhasatividades.html', {'atividades':atividades, 'tiposatividades':unique_tipo_obj, 'estados':unique_valida_obj, 'nomesquery':nome_query, 'tiposquery':tipo_query, 'estadosquery':estado_query})

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