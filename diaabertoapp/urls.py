from django.urls import path
from . import views
from diaabertoapp.views import index, atividades, edificios

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('atividades/', views.atividades, name='atividades'),
    path('minhasatividades/', views.minhasatividades, name='minhasatividades'),
    path('proporatividade/', views.proporatividade, name='proporatividade'),
    path('gestaoedificios/', views.edificios, name='gestaoedificios'),
]
