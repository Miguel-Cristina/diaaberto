"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import pytest
import django
from django.test import TestCase
from django.test.client import Client
from diaabertoapp.models import Utilizador, Tematica, TipoAtividade, PublicoAlvo, Sessao, Atividade, SessaoAtividade, Campus, Edificio, Sala, MaterialQuantidade, UnidadeOrganica, Departamento, UtilizadorTipo, DiaAberto
from diaabertoapp.forms import CampusForm,EdificioForm, SalaForm, UnidadeOrganicaForm, DepartamentoForm, PublicoAlvoForm, TematicasForm, TipoAtividadeForm, SessoesForm, AtividadeForm, MaterialQuantidadeForm, SessaoAtividadeForm
from . import views
import datetime
# TODO: Configure your database in settings.py and sync before running tests.

@pytest.mark.django_db
class ViewsTestCase(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewsTestCase, cls).setUpClass()
            django.setup()
            c = Client()
            c.login(username='admin',password="admin")


    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Página Inicial', 1, 200)

    def test_minhasatividades(self):

        response = self.client.get('/minhasatividades/')
        self.assertContains(response, 'Minhas Atividades', 2, 200)


@pytest.mark.django_db
class UnidadeOrganicaTestCase(TestCase):
    def setUp(self):
        self.objA = UnidadeOrganica.objects.create(nome="Faculdade de Ciências e Tecnologia")
        self.objB = UnidadeOrganica.objects.create(nome="Faculdade de Economia")
        
    def test_unidadesorganicas(self):
        
        self.assertEquals(self.objA.nome, 'Faculdade de Ciências e Tecnologia')       
        self.assertEquals(self.objB.nome, 'Faculdade de Economia')     
        
@pytest.mark.django_db
class DepartamentoTestCase(TestCase):
    def setUp(self):
        self.unidadeorganicaA = UnidadeOrganica.objects.create(nome="Faculdade de Ciências e Tecnologia")
        self.objA = Departamento.objects.create(nome="Departamento de Informática", unidadeorganica=self.unidadeorganicaA)

        
    def test_unidadesorganicas(self):
        
        self.assertEquals(self.objA.nome, 'Departamento de Informática') 
        self.assertEquals(self.objA.unidadeorganica.nome, 'Faculdade de Ciências e Tecnologia')       

@pytest.mark.django_db
class TematicaTestCase(TestCase):
    def setUp(self):
        self.objA = Tematica.objects.create(tema="Terapêutica")
        self.objB = Tematica.objects.create(tema="Informática")
        self.objC = Tematica.objects.create(tema="Gestão")
        self.objD = Tematica.objects.create(tema="Economia")
        self.objE = Tematica.objects.create(tema="Desporto")
        self.objF = Tematica.objects.create(tema="Ciências")
        self.objG = Tematica.objects.create(tema="Biologia")
        self.objH = Tematica.objects.create(tema="Arte")
    def test_tematicas(self):
        
        self.assertEquals(self.objA.tema, 'Terapêutica')       
        self.assertEquals(self.objB.tema, 'Informática')        
        self.assertEquals(self.objC.tema, 'Gestão')       
        self.assertEquals(self.objD.tema, 'Economia')        
        self.assertEquals(self.objE.tema, 'Desporto')        
        self.assertEquals(self.objF.tema, 'Ciências')     
        self.assertEquals(self.objG.tema, 'Biologia')
        self.assertEquals(self.objH.tema, 'Arte')
@pytest.mark.django_db
class TipoAtividadeTestCase(TestCase):
    def setUp(self):
        self.objA = TipoAtividade.objects.create(tipo="Atividades Experimentais")
        self.objB = TipoAtividade.objects.create(tipo="Atividades Tecnológicas")
        self.objC = TipoAtividade.objects.create(tipo="Conferências")
        self.objD = TipoAtividade.objects.create(tipo="Exposições")
        self.objE = TipoAtividade.objects.create(tipo="Feira das Exposições")
        self.objF = TipoAtividade.objects.create(tipo="Outras Atividades")
        self.objG = TipoAtividade.objects.create(tipo="Outras Atividades Culturais")
        self.objH = TipoAtividade.objects.create(tipo="Outras Atividades Desportivas")
        self.objI = TipoAtividade.objects.create(tipo="Outras Atividades Ensino")
        self.objJ = TipoAtividade.objects.create(tipo="Palestras")
        self.objK = TipoAtividade.objects.create(tipo="Passeios")
        self.objL = TipoAtividade.objects.create(tipo="Seminários")
        self.objM = TipoAtividade.objects.create(tipo="Tertúlias")
        self.objN = TipoAtividade.objects.create(tipo="Visitas Instalações")
        self.objO = TipoAtividade.objects.create(tipo="Visitas Laboratórios")
    def test_tiposatividades(self):
        
        self.assertEquals(self.objA.tipo, 'Atividades Experimentais')       
        self.assertEquals(self.objB.tipo, 'Atividades Tecnológicas')        
        self.assertEquals(self.objC.tipo, 'Conferências')       
        self.assertEquals(self.objD.tipo, 'Exposições')        
        self.assertEquals(self.objE.tipo, 'Feira das Exposições')        
        self.assertEquals(self.objF.tipo, 'Outras Atividades')     
        self.assertEquals(self.objG.tipo, 'Outras Atividades Culturais')
        self.assertEquals(self.objH.tipo, 'Outras Atividades Desportivas')
        self.assertEquals(self.objI.tipo, 'Outras Atividades Ensino')
        self.assertEquals(self.objJ.tipo, 'Palestras')
        self.assertEquals(self.objK.tipo, 'Passeios')
        self.assertEquals(self.objL.tipo, 'Seminários')
        self.assertEquals(self.objM.tipo, 'Tertúlias')
        self.assertEquals(self.objN.tipo, 'Visitas Instalações')
        self.assertEquals(self.objO.tipo, 'Visitas Laboratórios')
@pytest.mark.django_db
class PublicoAlvoTestCase(TestCase):
    def setUp(self):
        self.objA = PublicoAlvo.objects.create(nome="10º ano")
        self.objB = PublicoAlvo.objects.create(nome="11º ano")
        self.objC = PublicoAlvo.objects.create(nome="12º ano")
        self.objD = PublicoAlvo.objects.create(nome="Ciências e Tecnologia")
        self.objE = PublicoAlvo.objects.create(nome="Ciências Humanisticas")
        self.objF = PublicoAlvo.objects.create(nome="Ciências Socioeconómicas")
        self.objG = PublicoAlvo.objects.create(nome="Artes")
        self.objH = PublicoAlvo.objects.create(nome="Todos")
    def test_publicosalvos(self):
        
        self.assertEquals(self.objA.nome, '10º ano')       
        self.assertEquals(self.objB.nome, '11º ano')        
        self.assertEquals(self.objC.nome, '12º ano')       
        self.assertEquals(self.objD.nome, 'Ciências e Tecnologia')        
        self.assertEquals(self.objE.nome, 'Ciências Humanisticas')        
        self.assertEquals(self.objF.nome, 'Ciências Socioeconómicas')     
        self.assertEquals(self.objG.nome, 'Artes')
        self.assertEquals(self.objH.nome, 'Todos')
@pytest.mark.django_db
class SessaoTestCase(TestCase):
    def setUp(self):
        self.objA = Sessao.objects.create(hora="09:00")
        self.objB = Sessao.objects.create(hora="10:00")
        self.objC = Sessao.objects.create(hora="11:00")
        self.objD = Sessao.objects.create(hora="12:00")
        self.objE = Sessao.objects.create(hora="14:00")
        self.objF = Sessao.objects.create(hora="15:00")
        self.objG = Sessao.objects.create(hora="16:00")
        self.objH = Sessao.objects.create(hora="17:00")
    def test_sessoes(self):
        
        self.assertEquals(self.objA.hora, '09:00')       
        self.assertEquals(self.objB.hora, '10:00')        
        self.assertEquals(self.objC.hora, '11:00')       
        self.assertEquals(self.objD.hora, '12:00')        
        self.assertEquals(self.objE.hora, '14:00')        
        self.assertEquals(self.objF.hora, '15:00')     
        self.assertEquals(self.objG.hora, '16:00')
        self.assertEquals(self.objH.hora, '17:00')
@pytest.mark.django_db
class CampusTestCase(TestCase):
    def setUp(self):
        self.objA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.objB = Campus.objects.create(nome="Campus da Penha", morada="Penha", contacto="289100101")
        self.objC = Campus.objects.create(nome="Campus de Portimão", morada="Portimão", contacto="289100102")
    def test_campus(self):
        
        self.assertEquals(self.objA.nome, 'Campus das Gambelas')       
        self.assertEquals(self.objB.nome, 'Campus da Penha')        
        self.assertEquals(self.objC.nome, 'Campus de Portimão') 
    def test_moradacampus(self):
        
        self.assertEquals(self.objA.morada, 'Faro')       
        self.assertEquals(self.objB.morada, 'Penha')        
        self.assertEquals(self.objC.morada, 'Portimão') 
    def test_contactocampus(self):
        
        self.assertEquals(self.objA.contacto, '289100100')       
        self.assertEquals(self.objB.contacto, '289100101')        
        self.assertEquals(self.objC.contacto, '289100102') 
@pytest.mark.django_db
class EdificioTestCase(TestCase):
    def setUp(self):

        self.campusA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.objA = Edificio.objects.create(nome="Complexo Pedagógico", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objA.png")
        self.campusB = Campus.objects.create(nome="Campus da Penha", morada="Penha", contacto="289100101")
        self.objB = Edificio.objects.create(nome="Serviços Académicos", campus=self.campusB, mapa_imagem="diaabertoapp/maps/objB.png")
        self.objC = Edificio.objects.create(nome="C1", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objC.png")
        
    def test_edificio(self):
        
        self.assertEquals(self.objA.nome, 'Complexo Pedagógico')
        self.assertEquals(self.objB.nome, 'Serviços Académicos') 
        self.assertEquals(self.objC.nome, 'C1') 

    def test_edificiocampus(self):
        
        self.assertEquals(self.objA.campus, self.campusA)       
        self.assertEquals(self.objA.campus.nome, 'Campus das Gambelas')
        self.assertEquals(self.objB.campus, self.campusB)       
        self.assertEquals(self.objB.campus.nome, 'Campus da Penha')  
        self.assertEquals(self.objC.campus, self.campusA)       
        self.assertEquals(self.objC.campus.nome, 'Campus das Gambelas')  

    def test_mapa(self):
        
        self.assertEquals(self.objA.mapa_imagem, 'diaabertoapp/maps/objA.png')  
        self.assertEquals(self.objB.mapa_imagem, 'diaabertoapp/maps/objB.png')     
        self.assertEquals(self.objC.mapa_imagem, 'diaabertoapp/maps/objC.png')     
@pytest.mark.django_db
class SalaTestCase(TestCase):
    def setUp(self):

        self.campusA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.edificioA = Edificio.objects.create(nome="Complexo Pedagógico", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objA.png")
        self.objA = Sala.objects.create(identificacao="1.55",edificio = self.edificioA, mapa_imagem="diaabertoapp/maps/salaA.png")

        self.campusB = Campus.objects.create(nome="Campus da Penha", morada="Penha", contacto="289100101")
        self.edificioB = Edificio.objects.create(nome="Serviços Académicos", campus=self.campusB, mapa_imagem="diaabertoapp/maps/objB.png")
        self.objB = Sala.objects.create(identificacao="Anfiteatro A",edificio = self.edificioB, mapa_imagem="diaabertoapp/maps/salaB.png")

        
    def test_salas(self):
        
        self.assertEquals(self.objA.identificacao, '1.55')
        self.assertEquals(self.objB.identificacao, 'Anfiteatro A') 

    def test_salaedificio(self):
        
        self.assertEquals(self.objA.edificio, self.edificioA)       
        self.assertEquals(self.objA.edificio.nome, 'Complexo Pedagógico')
        self.assertEquals(self.objB.edificio, self.edificioB)       
        self.assertEquals(self.objB.edificio.nome, 'Serviços Académicos')  

    def test_salaedificiocampus(self):
        
        self.assertEquals(self.objA.edificio.campus, self.campusA)       
        self.assertEquals(self.objA.edificio.campus.nome, 'Campus das Gambelas')
        self.assertEquals(self.objB.edificio.campus, self.campusB)       
        self.assertEquals(self.objB.edificio.campus.nome, 'Campus da Penha')  

    def test_mapa(self):
        
        self.assertEquals(self.objA.mapa_imagem, 'diaabertoapp/maps/salaA.png')  
        self.assertEquals(self.objB.mapa_imagem, 'diaabertoapp/maps/salaB.png')     
 
@pytest.mark.django_db
class AtividadeTestCase(TestCase):
    def setUp(self):
        self.publicoalvoA = PublicoAlvo.objects.create(nome="10º ano")
        self.publicoalvoB = PublicoAlvo.objects.create(nome="11º ano")
        self.tipoatividadeA = TipoAtividade.objects.create(tipo="Palestras")
        self.unidadeorganicaA = UnidadeOrganica.objects.create(nome="Faculdade de Ciências e Tecnologia")
        self.departamentoA = Departamento.objects.create(unidadeorganica=self.unidadeorganicaA,nome="Departamento de Matemática")
        self.tematicaA=Tematica.objects.create(tema="Ciências")
        self.tematicaB=Tematica.objects.create(tema="Matemática")
        self.campusA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.edificioA = Edificio.objects.create(nome="Complexo Pedagógico", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objA.png")
        self.salaA = Sala.objects.create(identificacao="1.55",edificio = self.edificioA, mapa_imagem="diaabertoapp/maps/salaA.png")
        self.utilizadorTipoA = UtilizadorTipo.objects.create(tipo="Docente")
        self.utilizadorA = Utilizador.objects.create(nome="Paulo Águas", email="paguas@ualg.pt", utilizadortipo=self.utilizadorTipoA)
        self.objA = Atividade.objects.create(
            nome="Introdução à Matemática", 
            descricao="Vem descobrir o mundo da matemática financeira com o curso de Licenciatura com Mestrado Integrado de Matemática Financeira",
            duracao="50",
            limite_participantes="20",
            tipo_atividade=self.tipoatividadeA,
            unidadeorganica=self.unidadeorganicaA,
            departamento=self.departamentoA,
            campus=self.campusA,
            edificio=self.edificioA,
            sala=self.salaA,
            responsavel = self.utilizadorA)
        self.objA.tematicas.add(self.tematicaA)
        self.objA.tematicas.add(self.tematicaB)
        self.objA.publico_alvo.add(self.publicoalvoA)
        self.objA.publico_alvo.add(self.publicoalvoB)

    def test_atividades(self):
        
        self.assertEquals(self.objA.nome, 'Introdução à Matemática')      
        self.assertEquals(self.objA.descricao, 'Vem descobrir o mundo da matemática financeira com o curso de Licenciatura com Mestrado Integrado de Matemática Financeira')      
        self.assertEquals(self.objA.duracao, '50') 
        self.assertEquals(self.objA.limite_participantes, '20') 
        self.assertEquals(self.objA.tipo_atividade.tipo, 'Palestras') 
        self.assertEquals(self.objA.unidadeorganica.nome, 'Faculdade de Ciências e Tecnologia') 
        self.assertEquals(self.objA.departamento.nome, 'Departamento de Matemática') 
        self.assertEquals(self.objA.campus.nome, 'Campus das Gambelas') 
        self.assertEquals(self.objA.edificio.nome, 'Complexo Pedagógico') 
        self.assertEquals(self.objA.sala.identificacao, '1.55') 
        self.assertEquals(self.objA.responsavel.nome, 'Paulo Águas')
        self.assertEqual(self.objA.publico_alvo.all()[0].nome, "10º ano")
        self.assertEqual(self.objA.publico_alvo.all()[1].nome, "11º ano")
        self.assertEqual(self.objA.tematicas.all()[0].tema, "Ciências")
        self.assertEqual(self.objA.tematicas.all()[1].tema, "Matemática")
@pytest.mark.django_db
class MaterialQuantidadeTestCase(TestCase):

    def setUp(self):
        self.publicoalvoA = PublicoAlvo.objects.create(nome="10º ano")
        self.publicoalvoB = PublicoAlvo.objects.create(nome="11º ano")
        self.tipoatividadeA = TipoAtividade.objects.create(tipo="Palestras")
        self.unidadeorganicaA = UnidadeOrganica.objects.create(nome="Faculdade de Ciências e Tecnologia")
        self.departamentoA = Departamento.objects.create(unidadeorganica=self.unidadeorganicaA,nome="Departamento de Matemática")
        self.tematicaA=Tematica.objects.create(tema="Ciências")
        self.tematicaB=Tematica.objects.create(tema="Matemática")
        self.campusA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.edificioA = Edificio.objects.create(nome="Complexo Pedagógico", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objA.png")
        self.salaA = Sala.objects.create(identificacao="1.55",edificio = self.edificioA, mapa_imagem="diaabertoapp/maps/salaA.png")
        self.utilizadorTipoA = UtilizadorTipo.objects.create(tipo="Docente")
        self.utilizadorA = Utilizador.objects.create(nome="Paulo Águas", email="paguas@ualg.pt", utilizadortipo=self.utilizadorTipoA,)
        self.objA = Atividade.objects.create(
            nome="Introdução à Matemática", 
            descricao="Vem descobrir o mundo da matemática financeira com o curso de Licenciatura com Mestrado Integrado de Matemática Financeira",
            duracao="50",
            limite_participantes="20",
            tipo_atividade=self.tipoatividadeA,
            unidadeorganica=self.unidadeorganicaA,
            departamento=self.departamentoA,
            campus=self.campusA,
            edificio=self.edificioA,
            sala=self.salaA,
            responsavel = self.utilizadorA)
        self.objA.tematicas.add(self.tematicaA)
        self.objA.tematicas.add(self.tematicaB)
        self.objA.publico_alvo.add(self.publicoalvoA)
        self.objA.publico_alvo.add(self.publicoalvoB)
        self.materialObjA = MaterialQuantidade.objects.create(atividade=self.objA, material="Computador", quantidade="10")

    def test_materiaisquantidades(self):
        self.assertEqual(self.materialObjA.material, "Computador")
        self.assertEqual(self.materialObjA.quantidade, "10")
        self.assertEqual(self.materialObjA.atividade.nome, "Introdução à Matemática")

@pytest.mark.django_db
class SessaoAtividadeTestCase(TestCase):

    def setUp(self):
        self.publicoalvoA = PublicoAlvo.objects.create(nome="10º ano")
        self.publicoalvoB = PublicoAlvo.objects.create(nome="11º ano")
        self.tipoatividadeA = TipoAtividade.objects.create(tipo="Palestras")
        self.unidadeorganicaA = UnidadeOrganica.objects.create(nome="Faculdade de Ciências e Tecnologia")
        self.departamentoA = Departamento.objects.create(unidadeorganica=self.unidadeorganicaA,nome="Departamento de Matemática")
        self.tematicaA=Tematica.objects.create(tema="Ciências")
        self.tematicaB=Tematica.objects.create(tema="Matemática")
        self.campusA = Campus.objects.create(nome="Campus das Gambelas", morada="Faro", contacto="289100100")
        self.edificioA = Edificio.objects.create(nome="Complexo Pedagógico", campus=self.campusA, mapa_imagem="diaabertoapp/maps/objA.png")
        self.salaA = Sala.objects.create(identificacao="1.55",edificio = self.edificioA, mapa_imagem="diaabertoapp/maps/salaA.png")
        self.utilizadorTipoA = UtilizadorTipo.objects.create(tipo="Docente")
        self.utilizadorA = Utilizador.objects.create(nome="Paulo Águas", email="paguas@ualg.pt", utilizadortipo=self.utilizadorTipoA,)
        self.objA = Atividade.objects.create(
            nome="Introdução à Matemática", 
            descricao="Vem descobrir o mundo da matemática financeira com o curso de Licenciatura com Mestrado Integrado de Matemática Financeira",
            duracao="50",
            limite_participantes="20",
            tipo_atividade=self.tipoatividadeA,
            unidadeorganica=self.unidadeorganicaA,
            departamento=self.departamentoA,
            campus=self.campusA,
            edificio=self.edificioA,
            sala=self.salaA,
            responsavel = self.utilizadorA)
        self.objA.tematicas.add(self.tematicaA)
        self.objA.tematicas.add(self.tematicaB)
        self.objA.publico_alvo.add(self.publicoalvoA)
        self.objA.publico_alvo.add(self.publicoalvoB)
        self.sessaoA = Sessao.objects.create(hora="09:00")
        self.sessaoatividadeObjA = SessaoAtividade.objects.create(atividade=self.objA, dia="2020-02-02", sessao=self.sessaoA, numero_colaboradores="2")

    def test_sessaoatividades(self):


        self.assertEqual(self.sessaoatividadeObjA.dia, "2020-02-02")
        self.assertEqual(self.sessaoatividadeObjA.sessao.hora, "09:00")
        self.assertEqual(self.sessaoatividadeObjA.numero_colaboradores, "2")
        self.assertEqual(self.sessaoatividadeObjA.atividade.nome, "Introdução à Matemática")


@pytest.mark.django_db
class FormsTestCase(TestCase):

    def setUp(self):
        self.campusA = Campus.objects.create(nome='Campus das Gambelas', morada='Gambelas',contacto='289100100')
        self.edificioA = Edificio.objects.create(nome='Complexo 1', campus=self.campusA)
        self.salaA = Sala.objects.create(identificacao='Sala 2', edificio=self.edificioA)
        self.unidadeorganicaA = UnidadeOrganica.objects.create(nome='Faculdade de Literatura')
        self.departamentoA = Departamento.objects.create(nome='Departamento de Direitos Humanos', unidadeorganica=self.unidadeorganicaA)
        self.tematicaA=Tematica.objects.create(tema="Cozinha")
        self.tipoatividadeA=TipoAtividade.objects.create(tipo="Seminário")
        self.publicoalvoA = PublicoAlvo.objects.create(nome='Alunos do Basico')
        self.sessaoA = Sessao.objects.create(hora="13:50")
        self.utilizadorTipoA = UtilizadorTipo.objects.create(tipo="Docente")
        self.utilizadorA = Utilizador.objects.create(nome="Paulo Águas", email="paguas@ualg.pt", utilizadortipo=self.utilizadorTipoA,)
        self.atividadeA = Atividade.objects.create(
            nome="Introdução à Matemática", 
            descricao="Vem descobrir o mundo da matemática financeira com o curso de Licenciatura com Mestrado Integrado de Matemática Financeira",
            duracao="50",
            limite_participantes="20",
            tipo_atividade=self.tipoatividadeA,
            unidadeorganica=self.departamentoA.unidadeorganica,
            departamento=self.departamentoA,
            campus=self.salaA.edificio.campus,
            edificio=self.salaA.edificio,
            sala=self.salaA,
            responsavel = self.utilizadorA)
    def test_CampusForm(self):
        nome = 'Campus de Olhão'
        morada = 'Olhão'
        contacto = '289123456'
        form = CampusForm(data={'nome': nome,'morada' : morada, 'contacto' : contacto})
        self.assertTrue(form.is_valid())

    def test_CampusRepetido(self):
        nome = 'Campus das Gambelas'
        morada = 'Gambelas'
        contacto = '289100100'
        form = CampusForm(data={'nome': nome,'morada' : morada, 'contacto' : contacto})
        self.assertFalse(form.is_valid())
    
    def test_EdificioForm(self):
        nome = 'Complexo 7'
        form = EdificioForm(data={'nome': nome,'campus': self.campusA.id})
        self.assertTrue(form.is_valid())

    def test_EdificioRepetida(self):
        nome = 'Complexo 1'
        form = EdificioForm(data={'nome': nome,'campus': self.campusA.id})
        self.assertFalse(form.is_valid())

    def test_SalaForm(self):
        identificacao = 'Sala 1'
        form = SalaForm(data={'identificacao': identificacao,'campus': self.edificioA.campus.id, 'edificio': self.edificioA.id})
        self.assertTrue(form.is_valid())

    def test_SalaRepetida(self):
        identificacao = 'Sala 2'
        form = SalaForm(data={'identificacao': identificacao,'campus': self.edificioA.campus.id, 'edificio': self.edificioA.id})
        self.assertFalse(form.is_valid())

    def test_UnidadeOrganicaForm(self):
        nome = 'Faculdade de Direito'
        form = UnidadeOrganicaForm(data={'nome': nome})
        self.assertTrue(form.is_valid())

    def test_UnidadeOrganicaRepetido(self):
        nome = 'Faculdade de Literatura'
        form = UnidadeOrganicaForm(data={'nome': nome})
        self.assertFalse(form.is_valid())

    def test_DepartamentoForm(self):
        nome = 'Departamento de Direito'
        form = DepartamentoForm(data={'nome': nome, 'unidadeorganica':self.unidadeorganicaA.id})
        self.assertTrue(form.is_valid())

    def test_DepartamentoRepetido(self):
        nome = 'Departamento de Direitos Humanos'
        form = DepartamentoForm(data={'nome': nome, 'unidadeorganica':self.unidadeorganicaA.id})
        self.assertFalse(form.is_valid())

    def test_TematicasForm(self):
        tema = 'Linguas'
        form = TematicasForm(data={'tema': tema})
        self.assertTrue(form.is_valid())


    def test_TipoAtividadeForm(self):
        tipo = 'Aula'
        form = TipoAtividadeForm(data={'tipo':tipo})
        self.assertTrue(form.is_valid())

    def test_TipoAtividadeRepetido(self):
        tipo = 'Seminário'
        form = TipoAtividadeForm(data={'tipo':tipo})
        self.assertFalse(form.is_valid())

    def test_PublicoAlvoForm(self):
        nome = 'Alunos do Profissional'
        form = PublicoAlvoForm(data={'nome':nome})
        self.assertTrue(form.is_valid())

    def test_PublicoAlvoRepetido(self):
        nome = 'Alunos do Basico'
        form = PublicoAlvoForm(data={'nome':nome})
        self.assertFalse(form.is_valid())

    def test_SessoesForm(self):
        hora = '09:00'
        form = SessoesForm(data={'hora':hora})
        self.assertTrue(form.is_valid())

    def test_SessoesRepetido(self):
        hora = '13:50'
        form = SessoesForm(data={'hora':hora})
        self.assertFalse(form.is_valid())

    def test_AtividadeForm(self):

        form = AtividadeForm(data={'nome':"Atividade Teste", 'descricao':"Descricao da atividade teste.",
                                  'tipo_atividade': self.tipoatividadeA.id, 'limite_participantes':"25",
                                  'tematicas':[self.tematicaA], 'publico_alvo':[self.publicoalvoA], 'duracao':"45", 
                                  'unidadeorganica':self.departamentoA.unidadeorganica.id, 'departamento':self.departamentoA.id,
                                  'campus':self.salaA.edificio.campus.id, 'edificio':self.salaA.edificio.id, 'sala':self.salaA.id, 'data':"2020-01-01", 'validada':"PD", 'tipo_local':""})
        self.assertTrue(form.is_valid())

    def test_MaterialQuantidade(self):
        form = MaterialQuantidadeForm(data={'material':'Computador', 'quantidade':'10', 'atividade':self.atividadeA})
        self.assertTrue(form.is_valid())

    def test_SessaoAtividade(self):
        form = SessaoAtividadeForm(data={'dia':'2020-01-02', 'sessao':self.sessaoA.id, 'numero_colaboradores':'1', 'atividade':self.atividadeA.id})
        self.assertTrue(form.is_valid())