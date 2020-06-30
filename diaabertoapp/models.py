from django.db import models
import datetime
from django.forms import ModelForm
from django.utils import timezone


# Create your models here.


# ========================================================================================================================
# model Campus
# ========================================================================================================================
class Campus(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    morada = models.TextField(null=True)
    contacto = models.CharField(max_length=40)
    mapa_imagem = models.ImageField(upload_to='diaabertoapp/maps/', default='diaabertoapp/maps/default.png')

    # Métodos
    class Meta:
        db_table = 'Campus'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model UnidadeOrganica
# ========================================================================================================================
class UnidadeOrganica(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    campus = models.ForeignKey(Campus, models.DO_NOTHING, db_column='campus')

    class Meta:
        db_table = 'UnidadeOrganica'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model faculdade
# =====================================================================
class Faculdade(models.Model):
    nome = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'Faculdade'


# ========================================================================================================================
# model Departamento
# ========================================================================================================================
class Departamento(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    unidadeorganica = models.ForeignKey(UnidadeOrganica, on_delete=models.PROTECT)
    faculdade = models.ForeignKey(Faculdade, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model Edificio
# ========================================================================================================================
class Edificio(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=40)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True)
    mapa_imagem = models.ImageField(upload_to='diaabertoapp/maps/', default='diaabertoapp/maps/default.png')

    class Meta:
        db_table = 'Edificio'
        unique_together = (("nome", "campus"),)
        # Métodos

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model Sala
# ========================================================================================================================
class Sala(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    identificacao = models.CharField(max_length=40)
    edificio = models.ForeignKey(Edificio, on_delete=models.PROTECT, null=True)
    mapa_imagem = models.ImageField(upload_to='diaabertoapp/maps/', default='diaabertoapp/maps/default.png')

    class Meta:
        db_table = 'Sala'
        unique_together = (("identificacao", "edificio"),)
        # Métodos

    def __str__(self):
        return self.identificacao


# ========================================================================================================================
# model Tematica
# ========================================================================================================================
class Tematica(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    tema = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'Tematica'

    def __str__(self):
        return self.tema


# ========================================================================================================================
# model TipoAtividade
# ========================================================================================================================
class TipoAtividade(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'TipoAtividade'

    def __str__(self):
        return self.tipo


# ========================================================================================================================
# model PublicoAlvo
# ========================================================================================================================
class PublicoAlvo(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'PublicoAlvo'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model Sessao
# ========================================================================================================================
class Sessao(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    hora = models.TimeField(unique=True, null=True)

    class Meta:
        db_table = 'Sessao'

    # Métodos
    def get_hora(self):
        return self.hora

    def __str__(self):
        return str(self.hora)


# ========================================================================================================================
# model Material (desativado)
# ========================================================================================================================
class Material(models.Model):
    # Campos
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Material'

    # Métodos
    def __str__(self):
        return self.nome


# ========================================================================================================================
# model UtilizadorTipo
# ========================================================================================================================
class UtilizadorTipo(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'utilizadortipo'

    def __str__(self):
        return self.tipo


# ========================================================================================================================
# model Utilizador
# ========================================================================================================================
class Utilizador(models.Model):
    utilizadortipo = models.ForeignKey(UtilizadorTipo, models.DO_NOTHING)
    email = models.CharField(unique=True, max_length=255)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    numero_telemovel = models.IntegerField()
    cartao_cidadao = models.IntegerField()
    deficiencias = models.CharField(max_length=255)
    permitir_localizacao = models.IntegerField()
    utilizar_dados_pessoais = models.IntegerField()
    validado = models.IntegerField(blank=True, null=True)
    unidadeorganica = models.ForeignKey(UnidadeOrganica, models.DO_NOTHING, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'Utilizador'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model UtilizadorParticipante
# ========================================================================================================================
class UtilizadorParticipante(models.Model):
    id = models.AutoField(primary_key=True)
    utilizador = models.ForeignKey(Utilizador, on_delete=models.PROTECT, null=True)
    escola = models.CharField(max_length=255)
    area_estudos = models.CharField(max_length=255)
    ano_estudos = models.IntegerField(null=True, blank=True)
    checkin = models.IntegerField(null=True, blank=True)
    inscricao_id = models.IntegerField()

    class Meta:
        db_table = 'UtilizadorParticipante'

    def __str__(self):
        return self.utilizador.nome


# ========================================================================================================================
# model Atividade
# ========================================================================================================================
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
    REJEITADA = 'RJ'  # invalidada
    PENDENTE = 'PD'  # por validar
    VALIDADA = 'VD'  # validada
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

    # Métodos
    class Meta:
        db_table = 'Atividade'

    def get_tipo(self):
        return self.tipo_atividade

    def get_tipo_local(self):
        return self.tipo_local if self.tipo_local else 'Local não especificado'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model MaterialQuantidade
# ========================================================================================================================
class MaterialQuantidade(models.Model):
    atividade = models.ForeignKey('Atividade', related_name='material_quantidade', on_delete=models.CASCADE, null=True)
    material = models.CharField(max_length=255, null=True)
    quantidade = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'MaterialQuantidade'

    def __str__(self):
        return self.material


# ========================================================================================================================
# model SessaoAtividade
# ========================================================================================================================
class SessaoAtividade(models.Model):
    atividade = models.ForeignKey(Atividade, related_name='sessao_atividade', on_delete=models.CASCADE, null=True)
    sessao = models.ForeignKey(Sessao, on_delete=models.SET_NULL, null=True)
    dia = models.DateField(null=True)
    numero_colaboradores = models.PositiveSmallIntegerField(default=0, blank=True)
    n_alunos = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'SessaoAtividade'
        unique_together = (("atividade", "sessao", "dia"),)

    def __str__(self):
        return self.atividade.nome + ' ' + str(self.sessao.hora)


# ========================================================================================================================
# modelform AtividadeForm
# ========================================================================================================================
class AtividadeForm(ModelForm):
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao', 'duracao', 'limite_participantes', 'tipo_atividade', 'publico_alvo', 'data',
                  'unidadeorganica', 'departamento', 'validada', 'tematicas', 'campus', 'edificio', 'sala',
                  'tipo_local')


# ========================================================================================================================
# model Notificacao
# ========================================================================================================================
class Notificacao(models.Model):
    conteudo = models.TextField(blank=True, null=True)
    hora = models.DateTimeField()
    prioridade = models.IntegerField(blank=True, null=True)
    assunto = models.TextField(blank=True, null=True)
    utilizador_env = models.ForeignKey(Utilizador, models.DO_NOTHING, related_name='1+', null=True)
    utilizador_rec = models.ForeignKey(Utilizador, models.DO_NOTHING, related_name='1+', null=True)
    notificacao_grupo = models.IntegerField(db_column='Notificacao_grupo', null=True)
    visto = models.BooleanField(default=False)
    # visto

    class Meta:
        db_table = 'Notificacao'

        



# ========================================================================================================================
# model Dia
# ========================================================================================================================
class Dia(models.Model):
    dia = models.DateField(null=True)

    def __str__(self):
        return str(self.dia)

    class Meta:
        db_table = 'Dia'


# ========================================================================================================================
# model DiaAberto
# ========================================================================================================================
class DiaAberto(models.Model):
    titulo = models.CharField(max_length=255, null=True)
    descricao = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, null=True)
    contacto = models.IntegerField(null=True)
    data_inicio = models.DateField(null=True)
    data_fim = models.DateField(null=True)
    limite_inscricao_atividades = models.IntegerField()
    limite_inscricao_participantes = models.IntegerField()

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'DiaAberto'


# ========================================================================================================================
# model Escola
# ========================================================================================================================

class Escola(models.Model):
    nome = models.CharField(unique=True, max_length=255, blank=True, null=True)
    morada = models.TextField(blank=True, null=True)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True)
    contacto = models.IntegerField(blank=True, null=True)
    localidade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'escola'

    def __str__(self):
        return self.nome


# ========================================================================================================================
# model Inscricao
# ========================================================================================================================

class Inscricao(models.Model):
    dia = models.DateField()
    escola = models.ForeignKey(Escola, on_delete=models.DO_NOTHING, blank=True, null=True, db_column='escola_id')
    hora_check_in = models.TimeField()
    unidadeorganica_checkin = models.ForeignKey(UnidadeOrganica, on_delete=models.DO_NOTHING, db_column='unidadeorganica_checkin',
                                                blank=True, null=True)
    check_in = models.IntegerField(default=0)
    area_estudos = models.CharField(max_length=45)
    ano_estudos = models.IntegerField()
    utilizador = models.ForeignKey(Utilizador, on_delete=models.DO_NOTHING, db_column='utilizador')

    class Meta:
        db_table = 'inscricao'

    def __str__(self):
        return self.id.__str__()


# ========================================================================================================================
# model Colaboracao
# ========================================================================================================================
class Colaboracao(models.Model):
    colaborador = models.ForeignKey('Utilizador', models.DO_NOTHING)
    data_colaboracao = models.DateField(blank=True, null=True)
    hora_inicio_colab = models.TimeField(blank=True, null=True)
    hora_fim_colab = models.TimeField(blank=True, null=True)
    percurso = models.IntegerField(blank=True, null=True)
    sala_de_aula = models.IntegerField(blank=True, null=True)
    outras = models.IntegerField(blank=True, null=True)
    tarefa_atribuida = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'colaboracao'


# ========================================================================================================================
# model Tarefa
# ========================================================================================================================
class Tarefa(models.Model):
    id = models.AutoField(primary_key=True)

    REJEITADA = 'RJ'
    PORATRIBUIR = 'PA'
    ATRIBUIDA = 'AT'
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

    ATIVIDADE = 'AV'
    PERCURSO = 'PE'
    OUTRA = 'OT'

    TIPO_TAREFAS_CHOICES = (
        ('AV', 'Atividade'),
        ('PE', 'Percurso'),
        ('OT', 'Outra'),
    )
    tipo_tarefa = models.CharField(
        max_length=2,
        choices=TIPO_TAREFAS_CHOICES,
        default=ATIVIDADE
    )
    nome = models.CharField(max_length=255, null=True)
    descricao = models.CharField(max_length=255, null=True)
    localizacao_grupo = models.ForeignKey(Sala, related_name='tarefa_localizacao_grupo', on_delete=models.CASCADE,
                                          null=True, blank=True)
    atividade = models.ForeignKey(Atividade, related_name='tarefa_atividade', on_delete=models.CASCADE, null=True,
                                  blank=True)
    duracao = models.IntegerField(null=True)
    # duracao = models.TimeField(null=True)
    destino = models.ForeignKey(Sala, related_name='tarefa_destino', on_delete=models.CASCADE, null=True, blank=True)
    horario = models.TimeField(null=True)
    dia = models.DateField(default=datetime.date.today)
    cordenador = models.ForeignKey(Utilizador, related_name='gestor_tarefa', on_delete=models.CASCADE, null=True,
                                   blank=True)
    # coolaborador = models.ForeignKey( Utilizador , related_name='atribuicao_tarefa', on_delete=models.CASCADE, null=True,blank=True)
    coolaborador = models.ManyToManyField(Utilizador, related_name='tarefa_coolaborador')
    grupo = models.ManyToManyField(Inscricao, related_name='percurso_grupoM')
    colaboracao = models.ForeignKey(Colaboracao, on_delete=models.CASCADE, null=True)

    def str(self):
        return 'Tarefa : ' + self.id + ' Descricao : ' + self.descricao + self.coolaborador


# ========================================================================================================================
# model Transporte
# ========================================================================================================================
class Transporte(models.Model):
    tipo_transporte = models.CharField(max_length=255)
    numero = models.IntegerField()
    capacidade = models.IntegerField()

    class Meta:
        db_table = 'transporte'

    def __str__(self):
        return ('Numero={0},Tipo Transporte={1}, Capacidade={2}').format(str(self.numero), str(self.tipo_transporte),
                                                                         str(self.capacidade))


class Percurso(models.Model):
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)

    class Meta:
        db_table = 'percurso'

    def __str__(self):
        return ('Origem={0}, Destino={1}').format(str(self.origem), str(self.destino))


class Horario(models.Model):
    hora_chegada = models.TimeField()
    hora_partida = models.TimeField()
    data = models.DateField()

    class Meta:
        db_table = 'horario'

    def __str__(self):
        return ('Hora chegada={0}, Hora partida={1}, Data={2}').format(str(self.hora_chegada), str(self.hora_partida),
                                                                       str(self.data))


class Ementa(models.Model):
    preco_aluno_normal = models.DecimalField(max_digits=4, decimal_places=2)
    preco_outro_normal = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'ementa'


class Prato(models.Model):
    prato_carne = models.CharField(max_length=255)
    prato_peixe = models.CharField(max_length=255)
    prato_vegan = models.CharField(max_length=255)
    sopa = models.CharField(max_length=255, blank=True)
    sobremesa = models.CharField(max_length=255, blank=True)
    descricao = models.TextField()
    dia = models.DateField()
    ementa = models.ForeignKey(Ementa, models.DO_NOTHING)

    class Meta:
        db_table = 'prato'


class TransporteUniversitarioHorario(models.Model):
    horario = models.ForeignKey(Horario, models.DO_NOTHING)
    percurso = models.ForeignKey(Percurso, models.DO_NOTHING)
    transporte_universitario = models.ForeignKey(Transporte, models.DO_NOTHING)

    class Meta:
        db_table = 'transporte_universitario-horario'


class SessaoAtividadeInscricao(models.Model):
    id = models.AutoField(primary_key=True)
    sessaoAtividade = models.ForeignKey(SessaoAtividade, related_name='sessoes', on_delete=models.CASCADE)
    inscricao = models.ForeignKey(Inscricao, related_name='inscricoes', on_delete=models.CASCADE)
    numero_alunos = models.IntegerField()

    class Meta:
        db_table = 'SessaoAtividadeInscricao'

    def __str__(self):
        return str(self.id)


# -----------------------------------------------------------------------
# --------------------------------------------------------------------------


class EmentaInscricao(models.Model):
    ementa = models.ForeignKey(Ementa, models.DO_NOTHING)
    inscricao = models.ForeignKey('Inscricao', models.DO_NOTHING)
    numero_aluno_normal = models.IntegerField(blank=True, null=True)
    numero_outro_normal = models.IntegerField(blank=True, null=True)
    dia = models.DateField()

    class Meta:
        db_table = 'ementa_inscricao'

    def __str__(self):
        return self.inscricao


class Transporteproprio(models.Model):
    data = models.DateField()
    tipo_transporte = models.CharField(max_length=255)
    transporte_para_campus = models.CharField(max_length=255, null=True)
    transporte_entre_campus = models.CharField(max_length=255, null=True)
    hora_chegada = models.TimeField()
    hora_partida = models.TimeField()
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING)

    class Meta:
        db_table = 'transporteproprio'


class TransporteproprioPercursos(models.Model):
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    hora = models.TimeField()
    transporteproprio = models.ForeignKey(Transporteproprio, models.DO_NOTHING)

    class Meta:
        db_table = 'transporteproprio_percursos'

    def __str__(self):
        return self.origem + ' ' + self.destino


class InscricaoIndividual(models.Model):
    autorizacao = models.IntegerField(blank=True, null=True)
    ficheiro_autorizacao = models.CharField(max_length=255, blank=True, null=True)
    acompanhantes = models.IntegerField()
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING)

    class Meta:
        db_table = 'inscricao_individual'


class InscricaoGrupo(models.Model):
    total_participantes = models.IntegerField()
    total_professores = models.IntegerField()
    turma = models.CharField(max_length=255)
    inscricao = models.ForeignKey(Inscricao, models.DO_NOTHING)

    class Meta:
        db_table = 'inscricao_grupo'


# -------------------------------------------------------------------------------------


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    utilizador = models.ForeignKey('Utilizador', models.DO_NOTHING, db_column='utilizador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class UnidadeorganicaDepartamento(models.Model):
    unidade_organica = models.ForeignKey(UnidadeOrganica, models.DO_NOTHING, db_column='unidade_organica')
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='departamento')

    class Meta:
        db_table = 'unidadeorganica_departamento'


class UtilizadorTarefa(models.Model):
    tarefa = models.ForeignKey(Tarefa, models.DO_NOTHING)
    coordenador = models.ForeignKey(Utilizador, models.DO_NOTHING, related_name='1+')
    colaborador = models.ForeignKey(Utilizador, models.DO_NOTHING, blank=True, null=True, related_name='1+')
    colaboracao = models.ForeignKey(Colaboracao, models.DO_NOTHING)
    estado = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'utilizador_tarefa'

class TransporteUniversitarioinscricao(models.Model):
    percursos = models.ForeignKey(TransporteproprioPercursos, models.DO_NOTHING)
    transporte = models.ForeignKey(TransporteUniversitarioHorario, models.DO_NOTHING)

    class Meta:
        db_table = 'transporte_universitarioinscricao'
