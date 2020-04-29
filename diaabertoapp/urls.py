from django.urls import path
from . import views
from diaabertoapp.views import index, atividades, edificios
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('index/', views.index, name='index'),
    path('administrador/', views.administrador, name='administrador'),
    path('atividades/', views.atividades, name='atividades'),
    path('minhasatividades/', views.minhasatividades, name='minhasatividades'),
    path('minhasatividades/propor/', views.proporatividade, name='proporatividade'),
    #path('proporatividade/', views.proporatividade, name='proporatividade'),
    path('gestaoedificios/', views.edificios, name='gestaoedificios'),
    path('select2/', include('django_select2.urls')),
    path('tarefas/', views.get_tarefas, name='tarefas'),
    path('adicionartarefa/', views.add_tarefa, name='adicionartarefa'),
    path('tarefas/delete/<pk>',views.rem_tarefa, name='delete_tarefa'),
    path(r'^aceitaratividade/(?P<pk>[0-9]+)/$', views.aceitaratividade, name="aceitaratividade"),
    path(r'^rejeitaratividade/(?P<pk>[0-9]+)/$', views.rejeitaratividade, name="rejeitaratividade"),
    path('eliminaratividade/<pk>/', views.eliminaratividade, name="eliminaratividade"),
    path('alteraratividade/<pk>/',views.alteraratividade, name="alteraratividade"),
    path('administrador/configuraratividades/',views.configuraratividades, name="configuraratividades"),
    path('administrador/configuraratividades/sessoes',views.sessoes, name="configurarsessoes"),
    path('administrador/configuraratividades/publicoalvo',views.publicoalvo, name="configurarpublicoalvo"),
    path('administrador/configuraratividades/tematicas',views.tematicas, name="configurartematicas"),
    path('administrador/configuraratividades/tipoatividade',views.tipoatividade, name="configurartipoatividade"),
    path('administrador/configurarespacos/',views.configurarespacos, name="configurarespacos"),
    path('administrador/configurarespacos/campus',views.configurarcampus, name="configurarcampus"),
    path('administrador/configurarespacos/edificios',views.configuraredificios, name="configuraredificios"),
    path('administrador/configurarespacos/salas',views.configurarsalas, name="configurarsalas"),
    path('administrador/configurarespacos/eliminarsala/<pk>/', views.eliminarsala, name="eliminarsala"),
    path('administrador/configurarespacos/editarsala/<pk>/', views.editarsala, name="editarsala"),
    path('administrador/configurarespacos/adicionarsala/', views.adicionarsala, name="adicionarsala"),
    
]
