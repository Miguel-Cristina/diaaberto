from django.urls import path
from . import views
from diaabertoapp.views import index, atividades, edificios
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('atividades/', views.atividades, name='atividades'),
    path('minhasatividades/', views.minhasatividades, name='minhasatividades'),
    path('proporatividade/', views.proporatividade, name='proporatividade'),
    path('gestaoedificios/', views.edificios, name='gestaoedificios'),
    path('select2/', include('django_select2.urls')),
    path('tarefas/', views.get_tarefas, name='tarefas'),
    path(r'^aceitaratividade/(?P<pk>[0-9]+)/$', views.aceitaratividade, name="aceitaratividade"),
    path(r'^rejeitaratividade/(?P<pk>[0-9]+)/$', views.rejeitaratividade, name="rejeitaratividade"),
    path(r'^editaratividade/(?P<pk>[0-9]+)/$', views.editaratividade, name="editaratividade"),
]
