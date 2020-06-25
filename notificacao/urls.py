"""
LES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
#from django.contrib import admin
#from django.urls import path

#urlpatterns = [
    # Uncomment the next line to enable the admin:
    #path('admin/', admin.site.urls)
#]

from django.urls import path
from . import views
from .views import notificacao, Consultar_notificacao, Editar_notificacao

app_name = "notificacao"

urlpatterns = [
    path("notificacao/", notificacao.as_view(), name='notificacao'),
    path("consultar_notificacao/", Consultar_notificacao.as_view(), name='consultar_notificacao'),
    path("consultar_notificacao/editar_notificacao/<int:pk>", Editar_notificacao.as_view(), name='editar_notificacao'),
]