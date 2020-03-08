from django.urls import path
from . import views
from diaabertoapp.views import index, atividades

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('atividades/', views.atividades, name='atividades'),
]
