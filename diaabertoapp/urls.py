from django.urls import path
from . import views
from diaabertoapp.views import index
from django.conf.urls import include, handler404, handler500
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('error_500/', views.error_500, name='error_500'),
    path('error_404/', views.error_404, name='error_404'),
    path('', views.index, name='index'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('index/', views.index, name='index'),
    path('administrador/', views.administrador, name='administrador'),
    #path('atividades/', views.atividades, name='atividades'),
    path('minhasatividades/', views.minhasatividades, name='minhasatividades'),
    path('consultaratividades/', views.consultaratividades, name='consultaratividades'),
    path('minhasatividades/propor/', views.proporatividade, name='proporatividade'),
    #path('gestaoedificios/', views.edificios, name='gestaoedificios'),
    path('select2/', include('django_select2.urls')),
    path('tarefas/', views.get_tarefas, name='tarefas'),
    path('adicionartarefa/', views.add_tarefa, name='adicionartarefa'),
    path('tarefas/delete/<pk>',views.rem_tarefa, name='delete_tarefa'),
    path(r'^aceitaratividade/(?P<pk>[0-9]+)/$', views.aceitaratividade, name="aceitaratividade"),
    path(r'^rejeitaratividade/(?P<pk>[0-9]+)/$', views.rejeitaratividade, name="rejeitaratividade"),
    path('eliminaratividade/<pk>/', views.eliminaratividade, name="eliminaratividade"),
    path('alteraratividade/<pk>/',views.alteraratividade, name="alteraratividade"),
    path('visto/<pk>/',views.visto, name="visto"),
    path('sugeriralteracao/<pk>/',views.sugeriralteracao, name="sugeriralteracao"),


    path('configuraratividades/',views.configuraratividades, name="configuraratividades"),
    path('configuraratividades/sessoes/',views.sessoes, name="configurarsessoes"),
    path('configuraratividades/publicoalvo/',views.publicoalvo, name="configurarpublicoalvo"),
    path('configuraratividades/tematicas/',views.tematicas, name="configurartematicas"),
    path('configuraratividades/tipoatividade/',views.tipoatividade, name="configurartipoatividade"),


    path('configurarespacos/',views.configurarespacos, name="configurarespacos"),
    path('configurarespacos/campus/',views.configurarcampus, name="configurarcampus"),
    path('configurarespacos/edificios/',views.configuraredificios, name="configuraredificios"),
    path('configurarespacos/editaredificio/<pk>/', views.editaredificio, name="editaredificio"),
    path('configurarespacos/eliminaredificio/<pk>/', views.eliminaredificio, name="eliminaredificio"),
    path('configurarespacos/salas/',views.configurarsalas, name="configurarsalas"),
    path('configurarespacos/eliminarsala/<pk>/', views.eliminarsala, name="eliminarsala"),
    path('configurarespacos/editarsala/<pk>/', views.editarsala, name="editarsala"),
    path('configurarespacos/adicionarcampus/', views.adicionarcampus, name="adicionarcampus"),
    path('configurarespacos/eliminarcampus/<pk>/', views.eliminarcampus, name="eliminarcampus"),
    path('configurarespacos/editarcampus/<pk>/', views.editarcampus, name="editarcampus"),
    path('configurarespacos/adicionarsala/', views.adicionarsala, name="adicionarsala"),

    path('configurarespacos/adicionaredificio/', views.adicionaredificio, name="adicionaredificio"),
    path('configurarorganicasdepartamentos/',views.configurarorganicasdepartamentos, name="configurarorganicasdepartamentos"),
    path('configurarorganicasdepartamentos/organicas/',views.configurarorganicas, name="configurarorganicas"),
    path('configurarorganicasdepartamentos/eliminarorganica/<pk>/', views.eliminarorganica, name="eliminarorganica"),
    path('configurarorganicasdepartamentos/editarorganica/<pk>/', views.editarorganica, name="editarorganica"),
    path('configurarorganicasdepartamentos/adicionarorganica/', views.adicionarorganica, name="adicionarorganica"),
    path('configurarorganicasdepartamentos/departamentos/',views.configurardepartamentos, name="configurardepartamentos"),
    path('configurarorganicasdepartamentos/eliminardepartamento/<pk>/', views.eliminardepartamento, name="eliminardepartamento"),
    path('configurarorganicasdepartamentos/editardepartamento/<pk>/', views.editardepartamento, name="editardepartamento"),
    path('configurarorganicasdepartamentos/adicionardepartamento/', views.adicionardepartamento, name="adicionardepartamento"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)