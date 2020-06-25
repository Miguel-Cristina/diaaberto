from django.db import models

from diaabertoapp.models import Utilizador


class Notificacao(models.Model):
    conteudo = models.TextField(blank=True, null=True)
    hora = models.DateTimeField()
    prioridade = models.IntegerField(blank=True, null=True)
    assunto = models.TextField(blank=True, null=True)
    utilizador_env = models.ForeignKey(Utilizador, models.DO_NOTHING, related_name='utilizador_env')
    utilizador_rec = models.ForeignKey(Utilizador, models.DO_NOTHING, related_name='utilizador_rec')
    notificacao_grupo = models.IntegerField(db_column='Notificacao_grupo')

    class Meta:
        managed = False
        db_table = 'notificacoes'
