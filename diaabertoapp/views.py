from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'diaabertoapp/index.html', {})

def atividades(request):
    return render(request, 'diaabertoapp/atividades.html', {})

def minhasatividades(request):
    return render(request, 'diaabertoapp/minhasatividades.html', {})

def proporatividade(request):
    return render(request, 'diaabertoapp/proporatividade.html', {})