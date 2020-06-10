"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from diaabertoapp.models import Utilizador, Tematica, TipoAtividade
# TODO: Configure your database in settings.py and sync before running tests.



class TematicaTestCase(TestCase):
    def setUp(self):
        Tematica.objects.create(tema="Arte")
        Tematica.objects.create(tema="Biologia")
        Tematica.objects.create(tema="Ciências")
        Tematica.objects.create(tema="Desporto")
        Tematica.objects.create(tema="Economia")
        Tematica.objects.create(tema="Gestão")
        Tematica.objects.create(tema="Informática")
        Tematica.objects.create(tema="Saúde")
        Tematica.objects.create(tema="Terapêutica")

class TipoAtividadeTestCase(TestCase):
    def setUp(self):
        TipoAtividade.objects.create(tipo="Atividades Experimentais")
        TipoAtividade.objects.create(tipo="Atividades Tecnológicas")
        TipoAtividade.objects.create(tipo="Conferências")
        TipoAtividade.objects.create(tipo="Exposições")
        TipoAtividade.objects.create(tipo="Feira das Exposições")
        TipoAtividade.objects.create(tipo="Outras Atividades")
        TipoAtividade.objects.create(tipo="Outras Atividades Culturais")
        TipoAtividade.objects.create(tipo="Outras Atividades Desportivas")
        TipoAtividade.objects.create(tipo="Outras Atividades Ensino")
        TipoAtividade.objects.create(tipo="Palestras")
        TipoAtividade.objects.create(tipo="Passeios")
        TipoAtividade.objects.create(tipo="Seminários")
        TipoAtividade.objects.create(tipo="Tertúlias")
        TipoAtividade.objects.create(tipo="Visitas Instalações")
        TipoAtividade.objects.create(tipo="Visitas Laboratórios")

