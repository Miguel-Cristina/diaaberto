from django.db import models
import datetime
from django.forms import ModelForm
# Create your models here.


class Faculdade(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome
class Departamento(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class Campus(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    morada = models.TextField(null=True)
    contacto = models.CharField(max_length=40)
    
    #Métodos
    def get_absolute_url(self):
        return reverse('campus-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome


class Edificio(models.Model):
    # Campos
    id = models.AutoField(primary_key= True)
    nome = models.CharField(max_length=40)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,null=True)
    class Meta:
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
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE,null=True)
    class Meta:
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
    
    #Métodos
    def get_absolute_url(self):
        return reverse('tematica-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.tema

class PublicoAlvo(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)
    
    #Métodos
    def get_absolute_url(self):
        return reverse('tematica-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome

class Material(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=40, unique=True)
    
    #Métodos
    
    def __str__(self):
        return self.nome

class Atividade(models.Model):
 
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True)
    duracao = models.IntegerField()
    limite_participantes = models.IntegerField()

    VISITASINSTALACAO = 'VI' 
    VISITASLABORATORIO = 'VL'   
    ATIVIDADESEXPERIMENTAIS = 'AE'    
    ATIVIDADESTECNOLOGICAS = 'AT'
    FEIRACIENCIAS = 'FC'
    PALESTRAS = 'PL'
    CONFERENCIAS = 'CF'
    SEMINARIOS = 'SM'
    TERTULIAS = 'TT' 
    OUTRASENSINO = 'OE'
    OUTRASCULTURAIS = 'OC'
    OUTRASDESPORTIVAS = 'OD'
    EXPOSICOES = 'EX'
    PASSEIOS = 'PS'
    OUTRAS = 'OU'
    TIPO_ATIVIDADE_CHOICES = (
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
    tipo_atividade = models.CharField(
        max_length=2,
        choices=TIPO_ATIVIDADE_CHOICES
    )
    publico_alvo = models.ManyToManyField(PublicoAlvo, related_name='publico_alvo')
    data = models.DateField(default=datetime.date.today)
    faculdade = models.ForeignKey(Faculdade, on_delete=models.CASCADE, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
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
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)
    tipo_local = models.CharField(max_length=255, null=True, blank=True)
    #Métodos
    def get_absolute_url(self):
        return reverse('atividade-detail-view',args=[str(self.id)])

    def get_tipo(self):
        return self.tipo_atividade

    def get_tipo_local(self):
        return self.tipo_local if self.tipo_local else 'Local não especificado'

    def get_local(self):
        return self.local if self.local else 'Por atribuir (' + self.get_tipo_local() + ')'

    def __str__(self):
        return self.nome

class MaterialQuantidade(models.Model):

    atividade = models.ForeignKey('Atividade', related_name='material_quantidade', on_delete=models.SET_NULL, null=True)
    material = models.CharField(max_length=255, null=True)
    quantidade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.material + ' para ' + self.atividade.nome 



#class Local(models.Model):
#    id = models.AutoField(primary_key=True)
#    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE,null=True) #se o Edificio desaparecer, o local da atividade também desaparece, apesar deste campo ser por definição nulo (é tentador colocar models.DEFNULL, caso a chave estrangeira desapareça)
#    andar = models.CharField(max_length=30,null=True)
#    sala = models.CharField(max_length=30,null=True)
#    descricao = models.TextField(null=True, blank=True)
#    #Métodos
#    def get_absolute_url(self):
#        return reverse('localatividade-detail-view',args=[str(self.id)])
#    def __str__(self):
#        return self.edificio.campus.nome + ' Edificio ' + self.edificio.nome + ' Piso ' +self.andar + ' Sala ' + self.sala

#class LocalAtividade(models.Model):
#    id = models.AutoField(primary_key=True)
#    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True)
#    descricao = models.TextField(null=True, blank=True)
#    #Métodos
#
#    def __str__(self): 
#        if self.local:
#            return str(self.local)
#        elif self.descricao and not self.local:
#            return 'Outro local: ' + self.descricao
#        else:
#            return 'Por atribuir'

class AtividadeForm(ModelForm):
     class Meta:
         model = Atividade
         fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade','publico_alvo', 'data', 'faculdade', 'departamento', 'validada', 'tematicas', 'campus','edificio','sala', 'tipo_local')