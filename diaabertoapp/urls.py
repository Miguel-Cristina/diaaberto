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
    path('adicionartarefa/', views.add_tarefa, name='adicionartarefa'),
    path('tarefas/delete/<pk>',views.rem_tarefa, name='delete_tarefa'),
]
