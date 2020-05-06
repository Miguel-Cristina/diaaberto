from django.db import models
import datetime
from django.forms import ModelForm
# Create your models here.


class UnidadeOrganica(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table='UnidadeOrganica'
    def __str__(self):
        return self.nome
class Departamento(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    unidadeorganica = models.ForeignKey(UnidadeOrganica, on_delete=models.PROTECT)
    class Meta:
        db_table='Departamento'
    def __str__(self):
        return self.nome

class Campus(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    morada = models.TextField(null=True)
    contacto = models.CharField(max_length=40)
    
    #Métodos
    class Meta:
        db_table='Campus'
    def get_absolute_url(self):
        return reverse('campus-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome


class Edificio(models.Model):
    # Campos
    id = models.AutoField(primary_key= True)
    nome = models.CharField(max_length=40)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT,null=True)
    class Meta:
        db_table='Edificio'
        unique_together = (("nome", "campus"),) 
    #Métodos

    def get_absolute_url(self):
        return reverse('edificio-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome

class Sala(models.Model):
    # Campos
    id = models.AutoField(primary_key= True)
    identificacao = models.CharField(max_length=40)
    edificio = models.ForeignKey(Edificio, on_delete=models.PROTECT,null=True)
    class Meta:
        db_table='Sala'
        unique_together = (("identificacao", "edificio"),) 
    #Métodos
    def get_absolute_url(self):
        return reverse('edificio-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.identificacao


class Tematica(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    tema = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table='Tematica'
    #Métodos
    def get_absolute_url(self):
        return reverse('tematica-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.tema

class TipoAtividade(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table='TipoAtividade'
    #Métodos
    def get_absolute_url(self):
        return reverse('tipoatividade-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.tipo

class PublicoAlvo(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table='PublicoAlvo'
    #Métodos
    def get_absolute_url(self):
        return reverse('tematica-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome
class Sessao(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    hora = models.TimeField(unique=True,null=True)
    class Meta:
        db_table='Sessao'
    #Métodos
    def get_hora(self):
        return self.hora
    def __str__(self):
        return str(self.hora)

class Material(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    class Meta:
        db_table='Material'
    #Métodos
    def __str__(self):
        return self.nome

class UtilizadorTipo(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)
    class Meta:
        db_table='UtilizadorTipo'
    def __str__(self):
        return self.tipo

class Utilizador(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    utilizadortipo = models.ForeignKey(UtilizadorTipo, on_delete=models.PROTECT, null=True)
    nome = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    data_nascimento = models.DateField(null=True)
    numero_telemovel = models.CharField(max_length=255, null=True, blank=True)
    cartao_cidadao = models.CharField(max_length=255, null=True)
    deficiencias = models.CharField(max_length=255, null=True, blank=True)
    permitir_localizacao = models.IntegerField(null=True)
    utilizar_dados_pessoais = models.IntegerField(null=True)
    validado = models.IntegerField(null=True, blank=True)
    unidadeorganica = models.ForeignKey(UnidadeOrganica, on_delete=models.PROTECT, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table='Utilizador'

    def __str__(self):
        return self.nome

class UtilizadorParticipante(models.Model):
    id = models.AutoField(primary_key=True)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.PROTECT, null=True)
    escola = models.CharField(max_length=255)
    area_estudos = models.CharField(max_length=255)
    ano_estudos = models.IntegerField(null=True, blank=True)
    checkin = models.IntegerField(null=True, blank=True)
    inscricao_id = models.IntegerField()
    class Meta:
        db_table='UtilizadorParticipante'
    def __str__(self):
        return self.utilizador.nome


class Atividade(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True)
    duracao = models.IntegerField()
    limite_participantes = models.IntegerField()
    tipo_atividade = models.ForeignKey(TipoAtividade, on_delete=models.PROTECT, null=True)
    publico_alvo = models.ManyToManyField(PublicoAlvo, related_name='publico_alvo')
    data = models.DateField(default=datetime.date.today)
    unidadeorganica = models.ForeignKey(UnidadeOrganica, on_delete=models.PROTECT, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=True)
    REJEITADA = 'RJ'    #invalidada
    PENDENTE = 'PD'     #por validar
    VALIDADA = 'VD'     #validada
    VALIDACAO_CHOICES = [
        ('RJ', 'Rejeitada'),
        ('PD', 'Pendente'),
        ('VD', 'Validada'),
    ]
    validada = models.CharField(
        max_length=2,
        choices=VALIDACAO_CHOICES,
        default=PENDENTE,
    )
    tematicas = models.ManyToManyField(Tematica, related_name='temas')
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.PROTECT, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.PROTECT, null=True, blank=True)
    tipo_local = models.CharField(max_length=255, null=True, blank=True)
    responsavel = models.ForeignKey(Utilizador, on_delete=models.PROTECT, null=True, blank=True)
    #Métodos
    class Meta:
        db_table='Atividade'
    def get_tipo(self):
        return self.tipo_atividade

    def get_tipo_local(self):
        return self.tipo_local if self.tipo_local else 'Local não especificado'

    def __str__(self):
        return self.nome

class MaterialQuantidade(models.Model):

    atividade = models.ForeignKey('Atividade', related_name='material_quantidade', on_delete=models.CASCADE, null=True)
    material = models.CharField(max_length=255, null=True)
    quantidade = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table='MaterialQuantidade'
    def __str__(self):
        return self.material

class SessaoAtividade(models.Model):
    atividade = models.ForeignKey('Atividade', related_name='sessao_atividade', on_delete=models.CASCADE, null=True)
    sessao = models.ForeignKey('Sessao',on_delete=models.PROTECT, null=True)
    dia = models.DateField(null=True)
    numero_colaboradores = models.PositiveSmallIntegerField(default=0,blank=True)
    class Meta:
        db_table='SessaoAtividade'
        unique_together = (("atividade", "sessao", "dia"),) 
    def __str__(self):
        return self.atividade.nome

class AtividadeForm(ModelForm):
     class Meta:
         model = Atividade
         fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade','publico_alvo', 'data', 'unidadeorganica', 'departamento', 'validada', 'tematicas', 'campus','edificio','sala', 'tipo_local')


class Tarefa(models.Model):
     
    id = models.AutoField(primary_key=True)
     
    REJEITADA =   'RJ'
    PORATRIBUIR = 'PA'
    ATRIBUIDA =   'AT'
    VALIDACAO_CHOICES = [
        ('RJ', 'Rejeitada'),
        ('PA', 'Por Atribuir'),
        ('AT', 'Atribuida'),
    ]
    estado = models.CharField(
        max_length=2,
        choices=VALIDACAO_CHOICES,
        default=PORATRIBUIR,
    )

    ATIVIDADE = 'ATV' 
    PERCURSO =  'PE'   
    OUTRA    =  'OT'

    TIPO_TAREFAS_CHOICES = (
        ('AV', 'Atividade'),
        ('PE' , 'Percurso'),
        ('OT', 'Outra'),
    )
    tipo_tarefa = models.CharField(
        max_length=2,
        choices=TIPO_TAREFAS_CHOICES,
        default=ATIVIDADE
    )
    descricao = models.CharField(max_length=255, null=True)
    atividade = models.ForeignKey(Atividade, related_name='tarefa_atividade', on_delete=models.CASCADE, null=True,blank=True)
    localizacao_grupo = models.CharField(max_length=255, null=True)
    destino = models.CharField(max_length=255, null=True)
    horario = models.TimeField(null=True)
    dia = models.DateField(default=datetime.date.today)
    cordenador = models.IntegerField(default = 2)
    coolaborador = models.IntegerField(default = 3)

    def str(self):
        return 'Tarefa : ' + self.id + ' Descricao : '+ self.descricao
    class Meta:
        db_table='Tarefa'
        managed=True
