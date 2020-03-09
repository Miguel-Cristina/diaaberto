from django.shortcuts import render
from .models import Edificio

# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def minhasatividades(request):
    return render(request, 'diaabertoapp/minhasatividades.html', {})

def proporatividade(request):
    return render(request, 'diaabertoapp/proporatividade.html', {})

def edificios(request):
    edificios = Edificio.objects.all()
    return render(request, 'diaabertoapp/edificios.html', {'edificios':edificios})