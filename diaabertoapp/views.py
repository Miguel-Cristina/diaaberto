from django.shortcuts import render
from django.db.models import Count
from .models import Edificio, Atividade

# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def minhasatividades(request):
    minhasatividades = Atividade.objects.all()
    unique_tipo_obj = []
    unique_tipo_str = []
    unique_valida_obj = []
    unique_valida_str = []
    for x in minhasatividades:
        if x.tipo_atividade not in unique_tipo_str:
            unique_tipo_obj.append(x)
            unique_tipo_str.append(x.tipo_atividade)
        if x.validada not in unique_valida_str:
            unique_valida_obj.append(x)
            unique_valida_str.append(x.validada)
    estados = Atividade.objects.values('validada').distinct()
    return render(request, 'diaabertoapp/minhasatividades.html', {'atividades':minhasatividades, 'tiposatividades':unique_tipo_obj, 'estados':unique_valida_obj})

def proporatividade(request):
    return render(request, 'diaabertoapp/proporatividade.html', {})


def edificios(request):
    edificios = Edificio.objects.all()
    return render(request, 'diaabertoapp/edificios.html', {'edificios':edificios})