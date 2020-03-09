from django.db import models
import datetime
# Create your models here.


class Campus(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=40, unique=True)
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
    nome = models.CharField(max_length=40, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE,null=True)
    #Métodos
    def get_absolute_url(self):
        return reverse('edificio-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome + ' ('+ self.campus.nome + ')'

class LocalAtividade(models.Model):
    id = models.AutoField(primary_key=True)
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE,null=True) #se o Edificio desaparecer, o local da atividade também desaparece, apesar deste campo ser por definição nulo (é tentador colocar models.DEFNULL, caso a chave estrangeira desapareça)
    andar = models.CharField(max_length=30,null=True)
    sala = models.CharField(max_length=30,null=True)
    descricao = models.TextField(null=True, blank=True)
    #Métodos
    def get_absolute_url(self):
        return reverse('localatividade-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.edificio.campus.nome + ' Edificio ' + self.edificio.nome + ' Piso ' +self.andar + ' Sala ' + self.sala

class Tematica(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    tema = models.CharField(max_length=255, unique=True)
    
    #Métodos
    def get_absolute_url(self):
        return reverse('tematica-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.tema

class Atividade(models.Model):
 
    id = models.AutoField(primary_key=True)
    local = models.ForeignKey(LocalAtividade, on_delete=models.CASCADE,null=True) 
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
    TIPO_ATIVIDADE_CHOICES = [
        (VISITASINSTALACAO, 'Visitas Instalações'),
        (VISITASLABORATORIO , 'Visitas Laboratórios'),
        (ATIVIDADESEXPERIMENTAIS , 'Atividades Experimentais'),
	    (ATIVIDADESTECNOLOGICAS ,'Atividades Tencnológicas'),
	    (FEIRACIENCIAS ,'Feira das Ciências'),
	    (PALESTRAS ,'Palestras'),
	    (CONFERENCIAS ,'Conferências'),
	    (SEMINARIOS ,'Seminários'),
	    (TERTULIAS ,'Tertúlias'),
	    (OUTRASENSINO ,'Outras Atividades (Ensino)'),
	    (OUTRASCULTURAIS ,'Outras Atividades (Culturais)'),
	    (OUTRASDESPORTIVAS ,'Outras Atividades (Desportivas)'),
	    (EXPOSICOES ,'Exposições'),
	    (PASSEIOS ,'Passeios'),
	    (OUTRAS ,'Outras Atividades'),
    ]
    tipo_atividade = models.CharField(
        max_length=2,
        choices=TIPO_ATIVIDADE_CHOICES,
    )
    publico_alvo = models.CharField(max_length=45)
    data = models.DateField(default=datetime.date.today)
    
    REJEITADA = 'Rejeitada'    #invalidada
    PENDENTE = 'Pendente'     #por validar
    VALIDADA = 'Validada'     #validada
    VALIDACAO_CHOICES = [
        (REJEITADA, 'Rejeitada'),
        (PENDENTE, 'Pendente'),
        (VALIDADA, 'Validada'),
    ]
    validada = models.CharField(
        max_length=32,
        choices=VALIDACAO_CHOICES,
        default=PENDENTE,
    )
    
    #validada = models.BooleanField()

    #Métodos
    def get_absolute_url(self):
        return reverse('atividade-detail-view',args=[str(self.id)])

    def __str__(self):
        return self.nome