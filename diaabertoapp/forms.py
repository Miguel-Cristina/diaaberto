from django import forms
from .models import Atividade, Campus, Edificio, Sala, Tematica, PublicoAlvo, Faculdade, Departamento, MaterialQuantidade
import datetime


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

class AtividadeForm(forms.ModelForm):

    TIPOS_ATIVIDADES = {
        ('Selecione o tipo de atividade...',
         (
        ('VI', 'Visitas Instalações'),
        ('VL' , 'Visitas Laboratórios'),
        ('AE' , 'Atividades Experimentais'),
	    ('AT' ,'Atividades Tecnológicas'),
	    ('FC' ,'Feira das Ciências'),
	    ('PL' ,'Palestras'),
	    ('CF' ,'Conferências'),
	    ('SM' ,'Seminários'),
	    ('TT' ,'Tertúlias'),
	    ('OE' ,'Outras Atividades (Ensino)'),
	    ('OC' ,'Outras Atividades (Culturais)'),
	    ('OD' ,'Outras Atividades (Desportivas)'),
	    ('EX' ,'Exposições'),
	    ('PS' ,'Passeios'),
	    ('OU' ,'Outras Atividades'),
        )
         )}   

    nome = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Ex: Nome da atividade"}))
    tipo_atividade = forms.ChoiceField(label="",choices=TIPOS_ATIVIDADES, widget=forms.Select(attrs={'id': "tipoSearch"}))
    descricao = forms.CharField(label="", max_length=300, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea", 'id':"descricaoField",'onkeyup':"countChar(this)",'placeholder': "Ex: Descrição da atividade"}))
    limite_participantes = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'id':"maxPersons_input",'step':"1", 'type':"number",'placeholder':"0",'name':"numero_participantes_atividade"}))
    duracao = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'id':"duracao_input",'step':"5", 'type':"number",'placeholder':"0",'name':"duracao_atividade"}))
    tematicas = forms.MultipleChoiceField(choices=( (x.id, x.tema) for x in Tematica.objects.all() ), label="", widget=forms.SelectMultiple(attrs={'size':"4",'name':"tema_atividade"}))
    publico_alvo = forms.MultipleChoiceField(choices=( (x.id, x.nome) for x in PublicoAlvo.objects.all() ), label="", widget=forms.SelectMultiple(attrs={'size':"4",'name':"publico_alvo_atividade"}))
    #faculdade = forms.ChoiceField(label="",choices=( (x.id, x.nome) for x in Faculdade.objects.all() ), widget=forms.Select(attrs={'id': "faculdadeSearch",'name':"faculdade_atividade"}))
    #departamento = forms.ChoiceField(required=False,label="",choices=( (x.id, x.nome, x.faculdade.id) for x in Departamento.objects.all() ))
    tipo_local = forms.CharField(required=False, label="", max_length=255, widget=forms.TextInput(attrs={'type':"text", 'id':"tipoLocalinput", 'class':"input tipoLocalInput", 'placeholder':"ex: Sala grande/Laboratório",'name':"tipo_local_atividade"}))
    #campus = forms.ChoiceField(required=False,label="",choices=( (x.id, x.nome) for x in Campus.objects.all() ))
    #edificio = forms.ChoiceField(required=False,label="",choices=( (x.id, x.nome, x.campus.id) for x in Edificio.objects.all() ))
    #sala = forms.ChoiceField(required=False,label="",choices=( (x.id, x.identificacao, x.edificio.id) for x in Sala.objects.all() ))
    data = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    validada = forms.CharField(initial='PD', widget=forms.HiddenInput())
    
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade','publico_alvo', 'data', 'faculdade', 'departamento', 'validada', 'tematicas', 'campus','edificio','sala', 'tipo_local')

class MaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialQuantidade
        fields =  ('material', 'quantidade',)
