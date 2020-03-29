from django import forms
from .models import Atividade, Campus, Edificio, Sala, Tematica, PublicoAlvo, Faculdade, Departamento, MaterialQuantidade, Material
import datetime
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2.forms import ModelSelect2Widget

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
    tipo_atividade = forms.ChoiceField(label="",choices=TIPOS_ATIVIDADES, widget=forms.Select(attrs={'id': "tipoSearch", 'placeholder': "Escolha o tipo de atividade..."}))
    descricao = forms.CharField(label="", max_length=300, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea", 'id':"descricaoField",'onkeyup':"countChar(this)",'placeholder': "Ex: Descrição da atividade"}))
    limite_participantes = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'id':"maxPersons_input",'step':"1", 'type':"number",'placeholder':"0",'name':"numero_participantes_atividade"}))
    duracao = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'id':"duracao_input",'step':"5", 'type':"number",'placeholder':"0",'name':"duracao_atividade"}))
    tematicas = forms.MultipleChoiceField(choices=( (x.id, x.tema) for x in Tematica.objects.all() ), label="", widget=forms.SelectMultiple(attrs={'size':"4",'name':"tema_atividade"}))
    publico_alvo = forms.MultipleChoiceField(choices=( (x.id, x.nome) for x in PublicoAlvo.objects.all() ), label="", widget=forms.SelectMultiple(attrs={'size':"4",'name':"publico_alvo_atividade"}))
    tipo_local = forms.CharField(required=False, label="", max_length=255, widget=forms.TextInput(attrs={'type':"text", 'id':"tipoLocalinput", 'class':"input tipoLocalInput", 'placeholder':"ex: Sala grande/Laboratório",'name':"tipo_local_atividade"}))
    data = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    validada = forms.CharField(initial='PD', widget=forms.HiddenInput()) 
    faculdade = forms.ModelChoiceField(initial='2',queryset=Faculdade.objects.all(), label="",widget=ModelSelect2Widget(model=Faculdade,search_fields=['nome__icontains'],attrs={'id':"meuDepartamento",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione a faculdade..."})) 
    departamento = forms.ModelChoiceField(initial='2', queryset=Departamento.objects.all(), label="",widget=ModelSelect2Widget(model=Departamento,search_fields=['nome__icontains'],dependent_fields={'faculdade':'faculdade'},max_results=50,attrs={'id':"escolherDepartamento",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o departamento..."})) #'disabled':"true",
    campus = forms.ModelChoiceField(queryset=Campus.objects.all(), label="",widget=ModelSelect2Widget(model=Campus,search_fields=['nome__icontains'],attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o campus..."}))
    edificio = forms.ModelChoiceField(queryset=Edificio.objects.all(), label="",widget=ModelSelect2Widget(model=Edificio,search_fields=['nome__icontains'],dependent_fields={'campus':'campus'},attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o edificio..."}))
    sala = forms.ModelChoiceField(queryset=Sala.objects.all(), label="",widget=ModelSelect2Widget(model=Sala, search_fields=['identificacao__icontains'],dependent_fields={'edificio':'edificio'},attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione a sala..."}))
    #material = forms.Mult
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade','publico_alvo', 'data', 'faculdade', 'departamento', 'validada', 'tematicas', 'campus','edificio','sala', 'tipo_local')

class MaterialQuantidadeForm(forms.ModelForm):
    class Meta:
        model = MaterialQuantidade
        fields =  ('atividade','material', 'quantidade',)


