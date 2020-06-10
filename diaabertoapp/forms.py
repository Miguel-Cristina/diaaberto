from django import forms
from .models import Atividade, Campus, Edificio, Sala, Tematica, Dia, Tarefa, PublicoAlvo, UnidadeOrganica, Departamento, MaterialQuantidade, Material, Sessao, SessaoAtividade, TipoAtividade
import datetime
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2.forms import ModelSelect2Widget
from django.forms import formset_factory, modelformset_factory
from django.core.exceptions import NON_FIELD_ERRORS


class TarefaForm(forms.ModelForm):
     descricao =forms.CharField(label="", max_length=255, widget = forms.TextInput(attrs = {'class': "input", 'placeholder': "Descrição..."}))    
     localizacao_grupo = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Localização"}))
     destino = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Material a requisitar..."}))
     horario_inicio = forms.DateTimeField()
     horario_fim = forms.DateTimeField()
     cordenador = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"id_cordenadore"}))
     coolaborador = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"id_colaboradore"}))
     
     class Meta:
        model = Tarefa
        fields = ('descricao', 'localizacao_grupo' , 'destino' ,'horario_inicio', 'horario_fim', 'cordenador', 'coolaborador')

class CampusForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Campus"}),error_messages={'unique': 'Um campus com o mesmo nome já existe! Por favor coloque outro campus.'})
    morada = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Morada"}))
    contacto = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Contacto"}))
    
    class Meta:
        model = Campus
        fields = ('morada','contacto','nome',)

class EdificioForm(forms.ModelForm):
    campus = forms.ModelChoiceField(required=True, queryset=Campus.objects.all(), label="",widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}),error_messages={'unique_together':'Um edificio com esse nome já existe!','required':'Preencha este campo.','unique':'Um edificio com o mesmo nome já existe! Por favor coloque outro edificio.'})
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Edifício"}),error_messages={'unique_together':'Um edificio com esse nome já existe!', 'required':'Preencha este campo.','unique': 'Um edificio com o mesmo nome já existe! Por favor coloque outro edificio.'})
    mapa = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}))
    
    class Meta:
        model = Edificio
        fields = ('campus','nome','mapa',)
        error_messages = {

            NON_FIELD_ERRORS: {

                'unique_together': "O Edifício com este Nome e Campus já existe!",
            }

        }

class SalaForm(forms.ModelForm):
    campus = forms.ModelChoiceField(required=True,queryset=Campus.objects.all(), label="",widget=ModelSelect2Widget(model=Campus,search_fields=['nome__icontains'],attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o campus..."}))
    edificio = forms.ModelChoiceField(required=True,queryset=Edificio.objects.all(), label="",widget=ModelSelect2Widget(model=Edificio,search_fields=['nome__icontains'],dependent_fields={'campus':'campus'},attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o edificio..."}))
    identificacao = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Sala"}),error_messages={'unique': 'Uma sala com o mesmo nome já existe! Por favor coloque outra sala.'})
    mapa = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}))

    class Meta:
        model = Sala
        fields = ('campus','edificio', 'identificacao','mapa')
        error_messages = {

            NON_FIELD_ERRORS: {

                'unique_together': "A Sala com este Nome, Edifício e Campus já existe!",
            }

        }

class UnidadeOrganicaForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Uma unidade orgânica com o mesmo nome já existe! Por favor coloque outra unidade orgânica.'})
    class Meta:
        model = UnidadeOrganica
        fields = ('nome',)

class DepartamentoForm(forms.ModelForm):
    unidadeorganica = forms.ModelChoiceField(required=False, queryset=UnidadeOrganica.objects.all(), label="",widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%",'placeholder':"Selecione a unidade orgânica..."}))
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Uma unidade orgânica com o mesmo nome já existe! Por favor coloque outra unidade orgânica.'})
    class Meta:
        model = Departamento
        fields = ('unidadeorganica','nome',)

class PublicoAlvoForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um público-alvo com o mesmo nome já existe! Por favor coloque outro público-alvo.'})
    class Meta:
        model = PublicoAlvo
        fields = ('nome',)
        

class TematicasForm(forms.ModelForm):
    tema = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um tema com o mesmo nome já existe! Por favor coloque outro tema.'})
    class Meta:
        model = PublicoAlvo
        fields = ('tema',)

class TipoAtividadeForm(forms.ModelForm):
    tipo = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um tipo de atividade com o mesmo nome já existe! Por favor coloque outro tipo de atividade.'})
    class Meta:
        model = TipoAtividade
        fields = ('tipo',)

class SessoesForm(forms.ModelForm):
    hora = forms.TimeField(label="", widget=forms.TimeInput(attrs ={'class':"input timepicker control",'type':"time"}),error_messages={'unique': 'Uma sessão com a mesma hora já existe! Por favor coloque outra hora.'})
    class Meta:
        model = Sessao
        fields = ('hora',)

class MaterialQuantidadeForm(forms.ModelForm):
    material = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Material a requisitar..."}))
    quantidade = forms.IntegerField(min_value=1, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"quantidade_material"}))
    class Meta:
        model = MaterialQuantidade
        exclude =  ('atividade',)

MaterialFormSet = formset_factory(MaterialQuantidadeForm)

class SessaoAtividadeForm(forms.ModelForm):
    #dia = forms.DateField(required=False, label="Dia", widget=forms.DateInput(attrs={'class': "input", 'type':"date", 'placeholder': "Dia"}))
    dia = forms.ModelChoiceField(required=False, queryset=Dia.objects.all(), label="Dia",widget=forms.Select(attrs={'class':"select is-fullwidth sessoes",'style':"width:100%"}))
    sessao = forms.ModelChoiceField(required=False, queryset=Sessao.objects.all(), label="Sessao",widget=forms.Select(attrs={'class':"select is-fullwidth sessoes",'style':"width:100%"}),error_messages={'unique': 'Uma sessão com a mesma hora já existe! Por favor coloque outra hora.'})
    numero_colaboradores = forms.IntegerField(required=False, initial=0,min_value=0, label="Colaboradores", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"numero_colaboradores"}))
    class Meta:
        model = SessaoAtividade
        #exclude =  ('atividade',)
        fields = ('dia','sessao', 'numero_colaboradores')
        error_messages = {

            NON_FIELD_ERRORS: {

                'unique_together': "A sessão já existe! Escolha outra sessão ",
            }

        }
SessaoFormSet = formset_factory(SessaoAtividadeForm)

class AtividadeForm(forms.ModelForm):

    nome = forms.CharField(label="", max_length=255, required=True,widget=forms.TextInput(attrs={'class': "input tabfields",'placeholder': "Ex: Nome da atividade",'oninput':"$(this).removeClass('invalid');"}))
    descricao = forms.CharField(label="", max_length=300, required=True, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea tabfields", 'id':"descricaoField",'onkeyup':"countChar(this)",'placeholder': "Ex: Descrição da atividade",'oninput':"$(this).removeClass('invalid');"}))
    limite_participantes = forms.IntegerField(required=True, initial=0, min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input tabfields",'id':"maxPersons_input",'step':"1", 'type':"number",'placeholder':"0",'name':"numero_participantes_atividade",'onchange':"$(this).removeClass('invalid');"}))
    duracao = forms.IntegerField(required=True, initial=0, min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input tabfields",'id':"duracao_input",'step':"5", 'type':"number",'placeholder':"0",'name':"duracao_atividade",'onchange':"$(this).removeClass('invalid');"}))
    #tematicas = forms.MultipleChoiceField(choices=( (x.id, x.tema) for x in Tematica.objects.all() ), label="",required=True, widget=forms.SelectMultiple(attrs={'class':"tabfields",'size':"4",'name':"tema_atividade",'oninput':"$(this).removeClass('invalid');"}))
    #publico_alvo = forms.MultipleChoiceField(choices=( (x.id, x.nome) for x in PublicoAlvo.objects.all() ), label="", required=True, widget=forms.SelectMultiple(attrs={'class':"tabfields",'size':"4",'name':"publico_alvo_atividade",'oninput':"$(this).removeClass('invalid');"}))
    tematicas = forms.ModelMultipleChoiceField(required=True, queryset=Tematica.objects.all(), label="", widget=forms.SelectMultiple(attrs={'class':"input tabfields",'oninput':"$(this).removeClass('invalid');"}))
    publico_alvo = forms.ModelMultipleChoiceField(required=True, queryset=PublicoAlvo.objects.all(), label="", widget=forms.SelectMultiple(attrs={'class':"input tabfields",'oninput':"$(this).removeClass('invalid');"}))
    tipo_local = forms.CharField(required=False, label="", max_length=255, widget=forms.TextInput(attrs={'type':"text", 'id':"tipoLocalinput", 'class':"input tipoLocalInput tabfields", 'placeholder':"ex: Sala grande/Laboratório",'name':"tipo_local_atividade",'onchange':"$(this).removeClass('invalid');",'required':"true"}))
    data = forms.DateTimeField(initial=datetime.datetime.now, widget=forms.HiddenInput())
    validada = forms.CharField(initial='PD', widget=forms.HiddenInput()) 
    unidadeorganica = forms.ModelChoiceField(required=True, initial='2',queryset=UnidadeOrganica.objects.all(), label="",widget=ModelSelect2Widget(model=UnidadeOrganica,search_fields=['nome__icontains'],attrs={'class':"tabfields",'id':"meuDepartamento",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione a unidade orgânica...",'oninput':"$(this).removeClass('invalid');"})) 
    departamento = forms.ModelChoiceField(required=True, initial='1', queryset=Departamento.objects.all(), label="",widget=ModelSelect2Widget(model=Departamento,search_fields=['nome__icontains'],dependent_fields={'unidadeorganica':'unidadeorganica'},max_results=50,attrs={'class':"tabfields",'id':"escolherDepartamento",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o departamento..."})) #'disabled':"true",
    campus = forms.ModelChoiceField(required=False,queryset=Campus.objects.all(), label="",widget=ModelSelect2Widget(model=Campus,search_fields=['nome__icontains'],attrs={'class':"tabinputs escolhidoLocal",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o campus..."}))
    edificio = forms.ModelChoiceField(required=False,queryset=Edificio.objects.all(), label="",widget=ModelSelect2Widget(model=Edificio,search_fields=['nome__icontains'],dependent_fields={'campus':'campus'},attrs={'class':"tabinputs escolhidoLocal",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o edificio..."}))
    sala = forms.ModelChoiceField(required=False,queryset=Sala.objects.all(), label="",widget=ModelSelect2Widget(model=Sala, search_fields=['identificacao__icontains'],dependent_fields={'edificio':'edificio'},attrs={'class':"tabinputs escolhidoLocal",'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione a sala..."}))
    
    #material = forms.Mult
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade','publico_alvo', 'data', 'unidadeorganica', 'departamento', 'validada', 'tematicas', 'campus','edificio','sala', 'tipo_local')

    def __init__(self, *args, **kwargs):
        super(AtividadeForm, self).__init__(*args, **kwargs)
        #self.fields['tipo_atividade'].choices = [('', 'Selecione o tipo de atividade...')] + list(
        #    self.fields['tipo_atividade'].choices[1:])
        self.fields['tipo_atividade'].widget.attrs['class'] = 'tabfields'
        self.fields['tipo_atividade'].widget.attrs['onchange'] ="$(this).removeClass('invalid');"
    
      



#MaterialQuantidadeFormSet = inlineformset_factory(Atividade, MaterialQuantidade, form=MaterialQuantidadeForm)   



