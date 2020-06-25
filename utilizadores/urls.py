"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.urls import path
from . import views
from .views import register, Consultar_user, Editar_user

app_name = "Utilizadores"

urlpatterns = [

    path('admin/', admin.site.urls),
    path("register/", register.as_view(), name='add'),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("success/", views.success, name="success"),
    path("consultar_utilizadores/", Consultar_user.as_view(), name='consultar_user'),
    path("consultar_utilizadores/editar_utilizadores/<int:pk>/", Editar_user.as_view(), name='editar_user'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',
                                                                   success_url=reverse_lazy(
                                                                       'Utilizadores:password_change_done1')),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done1.html'),
         name='password_change_done1'),



]


