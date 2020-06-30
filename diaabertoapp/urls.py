from django.urls import path
from . import views
from diaabertoapp.views import index
from utilizadores.views import login_request, logout_request
from django.conf.urls import include, handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include

urlpatterns = [
    path('notificacoes/recebidas/', views.notificacoesrecebidas, name="notificacoes_recebidas"),

    path('error_500/', views.error_500, name='error_500'),
    path('error_404/', views.error_404, name='error_404'),
    path('', views.index, name='index'),
    path('utilizadores/login/', login_request, name='login'),
    path('utilizadores/logout/', logout_request, name='logout'),
    path('index/', views.index, name='index'),
    path('minhasatividades/', views.minhasatividades, name='minhasatividades'),
    path('consultaratividades/', views.consultaratividades, name='consultaratividades'),
    path('minhasatividades/propor/', views.proporatividade, name='proporatividade'),
    path('minhasatividades/alterar/<pk>/',views.alteraratividade, name="alteraratividade"),
    path('minhasatividades/eliminar/<pk>/', views.eliminaratividade, name="eliminaratividade"),
    path(r'^minhasatividades/aceitar/(?P<pk>[0-9]+)/$', views.aceitaratividade, name="aceitaratividade"),
    path(r'^minhasatividades/rejeitar/(?P<pk>[0-9]+)/$', views.rejeitaratividade, name="rejeitaratividade"),
    path('minhasatividades/sugeriralteracao/<pk>/',views.sugeriralteracao, name="sugeriralteracao"),
    path('select2/', include('django_select2.urls')),   
    path('visto/<pk>/',views.visto, name="visto"),
    path('configuraratividades/',views.configuraratividades, name="configuraratividades"),
    path('configuraratividades/sessoes/',views.sessoes, name="configurarsessoes"),
    path('configuraratividades/publicoalvo/',views.publicoalvo, name="configurarpublicoalvo"),
    path('configuraratividades/tematicas/',views.tematicas, name="configurartematicas"),
    path('configuraratividades/tipoatividade/',views.tipoatividade, name="configurartipoatividade"),
    path('configurarespacos/',views.configurarespacos, name="configurarespacos"),
    path('configurarespacos/edificios/',views.configuraredificios, name="configuraredificios"),
    path('configurarespacos/edificios/editar/<pk>/', views.editaredificio, name="editaredificio"),
    path('configurarespacos/edificios/eliminar/<pk>/', views.eliminaredificio, name="eliminaredificio"),
    path('configurarespacos/edificios/adicionar/', views.adicionaredificio, name="adicionaredificio"),
    path('configurarespacos/salas/',views.configurarsalas, name="configurarsalas"),
    path('configurarespacos/salas/adicionar/', views.adicionarsala, name="adicionarsala"),
    path('configurarespacos/salas/eliminar/<pk>/', views.eliminarsala, name="eliminarsala"),
    path('configurarespacos/salas/editar/<pk>/', views.editarsala, name="editarsala"),
    path('configurarespacos/campus/',views.configurarcampus, name="configurarcampus"),
    path('configurarespacos/campus/adicionar/', views.adicionarcampus, name="adicionarcampus"),
    path('configurarespacos/campus/eliminar/<pk>/', views.eliminarcampus, name="eliminarcampus"),
    path('configurarespacos/campus/editar/<pk>/', views.editarcampus, name="editarcampus"),
    path('configurarorganicasdepartamentos/',views.configurarorganicasdepartamentos, name="configurarorganicasdepartamentos"),
    path('configurarorganicasdepartamentos/organicas/',views.configurarorganicas, name="configurarorganicas"),
    path('configurarorganicasdepartamentos/organicas/eliminar/<pk>/', views.eliminarorganica, name="eliminarorganica"),
    path('configurarorganicasdepartamentos/organicas/editar/<pk>/', views.editarorganica, name="editarorganica"),
    path('configurarorganicasdepartamentos/organicas/adicionar/', views.adicionarorganica, name="adicionarorganica"),
    path('configurarorganicasdepartamentos/departamentos/',views.configurardepartamentos, name="configurardepartamentos"),
    path('configurarorganicasdepartamentos/departamentos/eliminar/<pk>/', views.eliminardepartamento, name="eliminardepartamento"),
    path('configurarorganicasdepartamentos/departamentos/editar/<pk>/', views.editardepartamento, name="editardepartamento"),
    path('configurarorganicasdepartamentos/departamentos/adicionar/', views.adicionardepartamento, name="adicionardepartamento"),

    path('tarefas/', views.get_tarefas, name='tarefas'),
    path('adicionartarefa/', views.add_tarefa, name='adicionartarefa'),
    path('tarefas/delete/<pk>',views.rem_tarefa, name='delete_tarefa'),
    path('tarefas/edit/<pk>',views.edit_tarefa, name='edit_tarefa'),
    path('tarefas/atribuir/<pk>',views.atribuir_tarefa, name='atribuir_tarefa'),
    path('tarefas/reatribuir/<pk>',views.remove_colab, name='remove_colab'),
    path(r'^ajax/grupos_switch/$', views.grupos_switch, name='grupos_switch'),
    path(r'^ajax/user_switch/$', views.user_switch, name='user_switch'),
    path(r'^ajax/activity_switch/$', views.activity_switch, name='activity_switch'),
    path(r'^ajax/sessions_switch/$', views.sessions_switch, name='sessions_switch'),

    path('configurartransporte/', views.configurartransporte, name='configurartransporte'),
    path('adicionartransporte/', views.adicionartransporte, name='adicionartransporte'),
    path('editartransporte/<int:id>/', views.editartransporte, name='editartransporte'),
    path('eliminartransporte/<int:id>/', views.eliminartransporte, name='eliminartransporte'),

    path('configurarpercurso/', views.configurarpercurso, name='configurarpercurso'),
    path('adicionarpercurso/', views.adicionarpercurso, name='adicionarpercurso'),
    path('editarpercurso/<int:id>/', views.editarpercurso, name='editarpercurso'),
    path('eliminarpercurso/<int:id>/', views.eliminarpercurso, name='eliminarpercurso'),

    path('configurarhorario/', views.configurarhorario, name='configurarhorario'),
    path('adicionarhorario/', views.adicionarhorario, name='adicionarhorario'),
    path('editarhorario/<int:id>/', views.editarhorario, name='editarhorario'),
    path('eliminarhorario/<int:id>/', views.eliminarhorario, name='eliminarhorario'),

    path('configurarprato/', views.configurarprato, name='configurarprato'),
    path('adicionarprato/', views.adicionarprato, name='adicionarprato'),
    path('editarprato/<int:id>/', views.editarprato, name='editarprato'),
    
    path('almocos/', views.almocos, name='almocos'),
    path('adicionarementa/', views.adicionarementa, name='adicionarementa'),
    path('editarementa/<int:id>/', views.editarementa, name='editarementa'),
    path('eliminarementa/<int:id>/', views.eliminarementa, name='eliminarementa'),

    path('transportes/', views.transportes, name='transportes'),
    path('adicionartransporteuniversitario/', views.adicionartransporteuniversitario, name='adicionartransporteuniversitario'),
    path('editartransporteuniversitario/<int:id>/', views.editartransporteuniversitario, name='editartransporteuniversitario'),
    path('eliminartransporteuniversitario/<int:id>/', views.eliminartransporteuniversitario, name='eliminartransporteuniversitario'),

    path('configurardiaaberto/', views.diaaberto, name='configurardiaaberto'),
    path('adicionarconfigurardiaaberto/', views.adicionardiaaberto, name='adicionarconfigurardiaaberto'),
    path('editarconfigurardiaaberto/<int:id>/', views.editardiaaberto, name='editarconfigurardiaaberto'),

    path('transporteinscricao/', views.transporteinscricao, name='transporteinscricao'),
    path('adicionartransporteinscricao/<int:id>/', views.adicionartransporteinscricao, name='adicionartransporteinscricao'),
    path('visualizartransporteinscricao/', views.vizualizartransporteinscricao, name='visualizartransporteinscricao'),
    path('editartransporteinscricao/<int:id>/', views.editartransporteinscricao, name='editartransporteinscricao')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#path(r'^aceitaratividade/(?P<pk>[0-9]+)/$', views.aceitaratividade, name="aceitaratividade"),
#path(r'^rejeitaratividade/(?P<pk>[0-9]+)/$', views.rejeitaratividade, name="rejeitaratividade"),
#path('sugeriralteracao/<pk>/',views.sugeriralteracao, name="sugeriralteracao"),
#path('configurarespacos/adicionaredificio/', views.adicionaredificio, name="adicionaredificio"),
#path('configurarespacos/editaredificio/<pk>/', views.editaredificio, name="editaredificio"),
#path('configurarespacos/eliminaredificio/<pk>/', views.eliminaredificio, name="eliminaredificio"),
#path('configurarespacos/adicionarcampus/', views.adicionarcampus, name="adicionarcampus"),
#path('configurarespacos/eliminarcampus/<pk>/', views.eliminarcampus, name="eliminarcampus"),
#path('configurarespacos/editarcampus/<pk>/', views.editarcampus, name="editarcampus"),
#path('configurarorganicasdepartamentos/eliminarorganica/<pk>/', views.eliminarorganica, name="eliminarorganica"),
#path('configurarorganicasdepartamentos/editarorganica/<pk>/', views.editarorganica, name="editarorganica"),
#path('configurarorganicasdepartamentos/adicionarorganica/', views.adicionarorganica, name="adicionarorganica"),
#path('configurarorganicasdepartamentos/departamentos/',views.configurardepartamentos, name="configurardepartamentos"),
#path('configurarorganicasdepartamentos/eliminardepartamento/<pk>/', views.eliminardepartamento, name="eliminardepartamento"),
#path('configurarorganicasdepartamentos/editardepartamento/<pk>/', views.editardepartamento, name="editardepartamento"),
#path('configurarorganicasdepartamentos/adicionardepartamento/', views.adicionardepartamento, name="adicionardepartamento"),