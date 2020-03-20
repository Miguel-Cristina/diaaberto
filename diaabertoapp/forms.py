from django import forms
from .models import Atividade, Campus, Edificio, Sala



class CampusForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    morada = forms.CharField(label='Morada', max_length=200)
    contacto = forms.CharField(label='Contacto', max_length=40)

class SalaForm(forms.ModelForm):
    campus = forms.ModelChoiceField(queryset=Campus.objects.all())
    edificio = forms.ModelChoiceField(queryset=Edificio.objects.none()) # Need to populate this using jquery
    sala = forms.ModelChoiceField(queryset=Sala.objects.none()) # Need to populate this using jquery

    class Meta:
        model = Sala

        fields = ('campus', 'edificio', 'sala')

    