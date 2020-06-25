from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from utilizadores.models import Utilizador

"""class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    utilizadortipo = forms.IntegerField(required=False, help_text='Optional.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'utilizadortipo', 'password1', 'password2')"""

'''CHOICES = (('Administrador', "ADMINISTRADOR"), ('Participante', "PARTICIPANTE"), ('Colaborador', "COLABORADOR"),
           ('Docente', "DOCENTE"), ('Coordenador', "COORDENADOR"))
CHOICES2 = (('Sim', "Sim"),
            ('Nao', "Nao"))'''

'''class Criar_Colab_Form(forms.Form):
    primeiro_dia = forms.CharField(label='primeiro_dia', widget=forms.RadioSelect(choices=CHOICES2))
    segundo_dia = forms.IntegerField(label='segundo_dia')
    sala_de_aula = forms.IntegerField(label='sala_de_aula')
    percurso = forms.IntegerField(label='percurso')'''

'''class Editar_Colab_Form(forms.Form):
    primeiro_dia = forms.CharField(label='primeiro_dia', widget=forms.RadioSelect(choices=CHOICES2))
    segundo_dia = forms.CharField(label='segundo_dia', widget=forms.RadioSelect(choices=CHOICES2))
    sala_de_aula = forms.CharField(label='sala_de_aula', widget=forms.RadioSelect(choices=CHOICES2))
    percurso = forms.CharField(label='percurso', widget=forms.RadioSelect(choices=CHOICES2))'''



