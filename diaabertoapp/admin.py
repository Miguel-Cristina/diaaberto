from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from diaabertoapp.models import SessaoAtividadeInscricao, Inscricao, Edificio, Campus, Transporte, Percurso, \
    TransporteUniversitarioHorario, Horario, Sala, Tematica, DiaAberto, Dia, Atividade, MaterialQuantidade, \
    UnidadeOrganica, Departamento, PublicoAlvo, Sessao, SessaoAtividade, TipoAtividade, Utilizador, UtilizadorTipo, \
    UtilizadorParticipante, Notificacao, Tarefa, Colaboracao
#LocalAtividade,Local
from django.utils.safestring import mark_safe
# Register your models here.


class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome', 'morada', 'contacto')
admin.site.register(Campus, CampusAdmin)


class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'campus')
admin.site.register(Edificio, EdificioAdmin)


class SalaAdmin(admin.ModelAdmin):
    list_display = ('identificacao', 'edificio', 'get_campus')
    def get_campus(self,obj):
        return obj.edificio.campus
admin.site.register(Sala, SalaAdmin)

admin.site.register(Tematica)

admin.site.register(Inscricao)

admin.site.register(SessaoAtividadeInscricao)

admin.site.register(Transporte)

admin.site.register(TransporteUniversitarioHorario)

admin.site.register(Percurso)

admin.site.register(Horario)

admin.site.register(PublicoAlvo)

admin.site.register(TipoAtividade)

admin.site.register(MaterialQuantidade)

admin.site.register(UnidadeOrganica)

admin.site.register(Departamento)

admin.site.register(Sessao)

admin.site.register(SessaoAtividade)

admin.site.register(Utilizador)

admin.site.register(UtilizadorTipo)

admin.site.register(UtilizadorParticipante)

admin.site.register(Notificacao)

admin.site.register(DiaAberto)

admin.site.register(Dia)

admin.site.register(Tarefa)

admin.site.register(Colaboracao)


class MateriaisInline(admin.TabularInline):
    model = MaterialQuantidade

class AtividadeAdmin(admin.ModelAdmin):
   
    list_display = ('nome', 'descricao', 'campus', 'edificio', 'sala', 'duracao', 'limite_participantes', 'tipo_atividade','colored_name')
    inlines = [
        MateriaisInline,
    ]

    def colored_name(self,obj):
        if obj.validada == 'VD':
            estado = 'Validada'
            cor = 'rgb(179, 255, 153)'
        elif obj.validada == 'RJ':
            estado = 'Rejeitada'
            cor = 'rgb(255, 153, 153)'
        else:
            estado = 'Pendente'
            cor = '	rgb(255, 255, 153)'
        return mark_safe('<div class="container" style="border-radius:5px;color:black; background:{};">{}</div>'.format(cor,estado))
    colored_name.allow_tags = True
    colored_name.short_description = 'Estado validação'
    colored_name.admin_order_field = 'validada'

admin.site.register(Atividade, AtividadeAdmin)