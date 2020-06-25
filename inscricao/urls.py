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

from django.urls import path
from . import views
from .views import HomeView, success, CriarInscricaoView, ConsultarInscricaoView, EditarInscricaoView

app_name = "inscricao"

urlpatterns = [
    path('criar/', CriarInscricaoView.as_view(), name='criar'),
    path('consultar/', ConsultarInscricaoView.as_view(), name='consultar'),
    path("consultar/editar/<int:pk>", EditarInscricaoView.as_view(), name='editarinscricao'),
    path('home/', HomeView.as_view(), name="home"),
    path('success/', success.as_view(), name="success"),
]
