from django import forms

class NotificacaoForm(forms.Form):
    conteudo =forms.CharField(label='conteudo',max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    #hora = forms.DateTimeField(label='hora')
    prioridade = forms.IntegerField(label='prioridade')
    assunto = forms.CharField(label='assunto',max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
    #utilizador_env = forms.IntegerField(label='utilizador_env' )
    #utilizador_rec = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    teste = forms.CharField(max_length=200, widget=forms.TextInput({}), required=False)

