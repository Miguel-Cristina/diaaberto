from django import forms
from .models import Prato, Ementa, Atividade, Campus, Edificio, Sala, Tematica, Dia, Tarefa, TransporteUniversitarioHorario, Transporte, Percurso, Horario, PublicoAlvo, UnidadeOrganica, Departamento, MaterialQuantidade, Material, Sessao, SessaoAtividade, TipoAtividade, DiaAberto, Utilizador, Inscricao
import datetime
from django.contrib.admin.widgets import AutocompleteSelect
from django_select2.forms import ModelSelect2Widget
from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.core.exceptions import NON_FIELD_ERRORS

#========================================================================================================================
# form do model Tarefa
#========================================================================================================================
class TarefaForm(forms.ModelForm):

     nome =forms.CharField(label="", max_length=255, widget = forms.TextInput(attrs = {'id':"nome",'class': "input", 'placeholder': "Insira um nome para a Tarefa"}))
     tipo_tarefa = forms.CharField(required = False, label ="",max_length=255, widget= forms.TextInput(attrs ={'class': 'input','type':'hidden','id':'tipo_tarefa'}))
     descricao =forms.CharField(required = False,label="", max_length=255, widget = forms.Textarea(attrs = {'id':"descricao",'class': "textarea", 'placeholder': "Descrição..."}))    
     localizacao_grupo = forms.ModelChoiceField(required=False, queryset=Sala.objects.all(), label="",widget=forms.Select(attrs={'id':'salaSearchEnc','class':"select is-fullwidth",'style':"width:100%"}))
     destino = forms.ModelChoiceField(required=False, queryset=Sala.objects.all(), label="",widget=forms.Select(attrs={'id':'salaSearchDesct','class':"select is-fullwidth",'style':"width:100%"}))
     dia = forms.DateField(required = False, label ="", widget= forms.TextInput(attrs ={'class': 'input','type':'date','id':'data'}))
     horario= forms.TimeField(required = False, label ="", widget= forms.TextInput(attrs ={'class': 'input','type':'time','id':'horas'}))
     atividade = forms.ModelChoiceField(required=False, queryset=Atividade.objects.all(), label="",widget=forms.Select(attrs={'id':'atividade','class':"select is-fullwidth",'style':"width:100%"}))
     coolaborador =forms.ModelMultipleChoiceField(required=False, queryset=Utilizador.objects.filter(utilizadortipo = 3),widget=forms.SelectMultiple(attrs={'id':'colaborador_id','class':"select is-multiple is-fullwidth",'style':"width:100%"}))
     grupo = forms.ModelMultipleChoiceField(required=False, queryset=Inscricao.objects.all(),widget=forms.SelectMultiple(attrs={'id':'gruposSelect','class':"select is-multiple is-fullwidth",'style':"width:100%",'label':"Grupo"}))
     duracao = forms.IntegerField(required=False, widget = forms.TextInput(attrs = {'class':'input','type':'number','step':'5','min':'0'}))
     
     class Meta:
        model = Tarefa
        fields = ('nome','descricao','tipo_tarefa','duracao', 'localizacao_grupo' , 'destino' ,'horario', 'atividade','dia','grupo','coolaborador')
#========================================================================================================================
# form do model Campus
#========================================================================================================================
class CampusForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Campus"}),error_messages={'unique': 'Um campus com o mesmo nome já existe! Por favor coloque outro campus.'})
    morada = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Morada"}))
    contacto = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Contacto"}))
    
    class Meta:
        model = Campus
        fields = ('morada','contacto','nome','mapa_imagem',)
#========================================================================================================================
# form do model Edificio
#========================================================================================================================
class EdificioForm(forms.ModelForm):
    campus = forms.ModelChoiceField(required=True, queryset=Campus.objects.all(), label="",widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}),error_messages={'unique_together':'Um edificio com esse nome já existe!','required':'Preencha este campo.','unique':'Um edificio com o mesmo nome já existe! Por favor coloque outro edificio.'})
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Edifício"}),error_messages={'unique_together':'Um edificio com esse nome já existe!', 'required':'Preencha este campo.','unique': 'Um edificio com o mesmo nome já existe! Por favor coloque outro edificio.'})
    mapa = forms.CharField(required=False, label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}))
    
    class Meta:
        model = Edificio
        fields = ('campus','nome','mapa_imagem',)
        error_messages = {

            NON_FIELD_ERRORS: {

                'unique_together': "O Edifício com este Nome e Campus já existe!",
            }

        }
#========================================================================================================================
# form do model Sala
#========================================================================================================================
class SalaForm(forms.ModelForm):
    campus = forms.ModelChoiceField(required=True,queryset=Campus.objects.all(), label="",widget=ModelSelect2Widget(model=Campus,search_fields=['nome__icontains'],attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o campus..."}))
    edificio = forms.ModelChoiceField(required=True,queryset=Edificio.objects.all(), label="",widget=ModelSelect2Widget(model=Edificio,search_fields=['nome__icontains'],dependent_fields={'campus':'campus'},attrs={'style':"width:100%",'data-minimum-input-length':"0",'data-placeholder':"Selecione o edificio..."}))
    identificacao = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text",'placeholder':"Sala"}),error_messages={'unique': 'Uma sala com o mesmo nome já existe! Por favor coloque outra sala.'})
    mapa = forms.CharField(required=False,label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}))

    class Meta:
        model = Sala
        fields = ('campus','edificio', 'identificacao','mapa','mapa_imagem')
        error_messages = {

            NON_FIELD_ERRORS: {

                'unique_together': "A Sala com este Nome, Edifício e Campus já existe!",
            }

        }
#========================================================================================================================
# form do model UnidadeOrganica
#========================================================================================================================
class UnidadeOrganicaForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Uma unidade orgânica com o mesmo nome já existe! Por favor coloque outra unidade orgânica.'})
    campus = forms.ModelChoiceField(required=True, queryset=Campus.objects.all(), label="", widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%",'placeholder':"Selecione o campus..."}))
    class Meta:
        model = UnidadeOrganica
        fields = ('nome','campus', )
#========================================================================================================================
# form do model Departamento
#========================================================================================================================
class DepartamentoForm(forms.ModelForm):
    unidadeorganica = forms.ModelChoiceField(queryset=UnidadeOrganica.objects.all(), label="",widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%",'placeholder':"Selecione a unidade orgânica..."}))
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Uma unidade orgânica com o mesmo nome já existe! Por favor coloque outra unidade orgânica.'})
    class Meta:
        model = Departamento
        fields = ('unidadeorganica','nome',)
#========================================================================================================================
# form do model PublicoAlvo
#========================================================================================================================
class PublicoAlvoForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um público-alvo com o mesmo nome já existe! Por favor coloque outro público-alvo.'})
    class Meta:
        model = PublicoAlvo
        fields = ('nome',)
        
#========================================================================================================================
# form do model Tematicas
#========================================================================================================================
class TematicasForm(forms.ModelForm):
    tema = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um tema com o mesmo nome já existe! Por favor coloque outro tema.'})
    class Meta:
        model = PublicoAlvo
        fields = ('tema',)
#========================================================================================================================
# form do model TipoAtividade
#========================================================================================================================
class TipoAtividadeForm(forms.ModelForm):
    tipo = forms.CharField(label="", widget=forms.TextInput(attrs ={'class':"input",'type':"text"}),error_messages={'unique': 'Um tipo de atividade com o mesmo nome já existe! Por favor coloque outro tipo de atividade.'})
    class Meta:
        model = TipoAtividade
        fields = ('tipo',)
#========================================================================================================================
# form do model Sessao
#========================================================================================================================
class SessoesForm(forms.ModelForm):
    hora = forms.TimeField(label="", widget=forms.TimeInput(attrs ={'class':"input timepicker control",'type':"time"}),error_messages={'unique': 'Uma sessão com a mesma hora já existe! Por favor coloque outra hora.'})
    class Meta:
        model = Sessao
        fields = ('hora',)
#========================================================================================================================
# form do model MaterialQuantidade
#========================================================================================================================
class MaterialQuantidadeForm(forms.ModelForm):
    material = forms.CharField(label="", max_length=255, widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Material a requisitar..."}))
    quantidade = forms.IntegerField(min_value=1, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"quantidade_material"}))
    class Meta:
        model = MaterialQuantidade
        exclude =  ('atividade',)

MaterialFormSet = formset_factory(MaterialQuantidadeForm)
#========================================================================================================================
# form do model SessaoAtividade
#========================================================================================================================
class SessaoAtividadeForm(forms.ModelForm):

    dia = forms.DateField(required=False, label="Dia", widget=forms.DateInput(attrs={'class': "input sessoes tabfields", 'type':"date", 'placeholder': "Dia", 'oninput':"$(this).removeClass('invalid');"}))
    #dia = forms.ModelChoiceField(required=False, queryset=Dia.objects.all(), label="Dia",widget=forms.Select(attrs={'class':"select is-fullwidth sessoes tabfields",'style':"width:100%",'oninput':"$(this).removeClass('invalid');"}))
    sessao = forms.ModelChoiceField(required=False, queryset=Sessao.objects.all(), label="Sessao",widget=forms.Select(attrs={'class':"select is-fullwidth sessoes tabfields",'style':"width:100%"}),error_messages={'unique': 'Uma sessão com a mesma hora já existe! Por favor coloque outra hora.'})
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
    def __init__(self, *args, **kwargs):
        super(SessaoAtividadeForm, self).__init__(*args, **kwargs)
        try:
            diaaberto = DiaAberto.objects.first()
        except DiaAberto.DoesNotExist:
            diaaberto = None
        if diaaberto is not None:
            data_inicio = diaaberto.data_inicio
            data_fim = diaaberto.data_fim
        else:
            data_inicio = '2001-01-01'
            data_fim = '2001-01-01'
        self.fields['dia'].widget.attrs.update({
                'min': data_inicio,
                'max': data_fim
            })
SessaoFormSet = formset_factory(SessaoAtividadeForm)

#========================================================================================================================
# form do model Atividade
#========================================================================================================================
class AtividadeForm(forms.ModelForm):

    nome = forms.CharField(label="", max_length=255, required=True,widget=forms.TextInput(attrs={'class': "input tabfields",'placeholder': "Ex: Nome da atividade",'oninput':"$(this).removeClass('invalid');"}))
    descricao = forms.CharField(label="", max_length=300, required=True, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea tabfields", 'id':"descricaoField",'onkeyup':"countChar(this)",'placeholder': "Ex: Descrição da atividade",'oninput':"$(this).removeClass('invalid');"}))
    limite_participantes = forms.IntegerField(required=True, initial=0, min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input tabfields",'id':"maxPersons_input",'step':"1", 'type':"number",'placeholder':"0",'name':"numero_participantes_atividade",'onchange':"$(this).removeClass('invalid');"}))
    duracao = forms.IntegerField(required=True, initial=0, min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input tabfields",'id':"duracao_input",'step':"1", 'type':"number",'placeholder':"0",'name':"duracao_atividade",'onchange':"$(this).removeClass('invalid');"}))
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

class TransporteForm(forms.ModelForm):
    tipo_transporte = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Tipo de Transporte"}))
    numero = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"Numero"}))
    capacidade = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"Numero"}))
    class Meta:
        model = Transporte
        fields = ('tipo_transporte', 'numero', 'capacidade')

class PercursoForm(forms.ModelForm):
    origem = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Origem do transporte"}))
    destino = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Destino do transporte"}))
    
    class Meta:
        model = Percurso
        fields = ('origem', 'destino')

class HorarioForm(forms.ModelForm):
    hora_chegada = forms.TimeField(widget= forms.TimeInput(attrs ={'class': 'input','type':'time'}))
    hora_partida = forms.TimeField(widget= forms.TimeInput(attrs ={'class': 'input','type':'time'}))
    data = forms.DateTimeField(widget= forms.DateInput(attrs ={'class': 'input','type':'date'}))
    
    class Meta:
        model = Horario
        fields = ('hora_chegada', 'hora_partida', 'data')

class EmentaForm(forms.ModelForm):
    prato = forms.ModelChoiceField(queryset=Prato.objects.all(), widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}))
    dia = forms.DateTimeField(widget= forms.DateInput(attrs ={'class': 'input','type':'date'}))
    preco_aluno_normal = forms.DecimalField(max_digits=4, decimal_places=2)
    preco_aluno_economico = forms.DecimalField(max_digits=4, decimal_places=2)
    preco_outro = forms.DecimalField(max_digits=4, decimal_places=2)
    preco_outro_economico = forms.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        model = Ementa
        fields=('prato', 'dia', 'preco_aluno_normal', 'preco_aluno_economico', 'preco_outro', 'preco_outro_economico')
    
class PratoForm(forms.ModelForm):
    nome = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Nome do Prato"}))
    tipo = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Tipo Prato"}))
    descricao = forms.CharField(label="", max_length=300, required=True, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea tabfields", 'id':"descricaoField",'placeholder': "Ex: Descrição do Prato"}))
    sopa = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Sopa"}))
    sobremesa = tipo = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Sobremesa"}))

    class Meta:
        model = Prato
        fields = ('nome', 'tipo', 'descricao', 'sopa', 'sobremesa')

class DiaabertoForm(forms.ModelForm):
    titulo = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "Titulo"}))
    email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "input", 'placeholder': "email"}))
    contacto = forms.IntegerField(min_value=0, label="", widget=forms.NumberInput(attrs={'class':"input",'step':"1", 'type':"number",'placeholder':"0",'name':"Numero"}))
    data_inicio = forms.DateTimeField(widget= forms.DateInput(attrs ={'class': 'input','type':'date'}))
    data_fim = forms.DateTimeField(widget= forms.DateInput(attrs ={'class': 'input','type':'date'}))
    descricao = forms.CharField(label="", max_length=1200, required=True, widget=forms.Textarea(attrs={'rows':"3",'class': "textarea tabfields", 'id':"descricaoField",'placeholder': "Ex: Descrição do Dia Aberto"}))
    

    class Meta:
        model = DiaAberto
        fields = ('titulo', 'email', 'contacto', 'data_inicio', 'data_fim', 'descricao')

class TransporteUniversitarioHorarioForm(forms.ModelForm):
    percurso = forms.ModelChoiceField(queryset=Percurso.objects.all(), widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}))
    horario = forms.ModelChoiceField(queryset=Horario.objects.all(), widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}))
    transporte_universitario = forms.ModelChoiceField(queryset=Transporte.objects.all(), widget=forms.Select(attrs={'class':"select is-fullwidth",'style':"width:100%"}))


    class Meta:
        model = TransporteUniversitarioHorario
        fields = ('transporte_universitario', 'horario', 'percurso')


