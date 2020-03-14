from django import forms

class CampusForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    morada = forms.CharField(label='Morada', max_length=200)
    contacto = forms.CharField(label='Contacto', max_length=40)
