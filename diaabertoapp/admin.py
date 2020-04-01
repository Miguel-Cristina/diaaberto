from django.contrib import admin
from diaabertoapp.models import Edificio, Campus, Sala, Tematica, Atividade, MaterialQuantidade, Faculdade, Departamento, PublicoAlvo, Sessao, SessaoAtividade
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

admin.site.register(PublicoAlvo)

#admin.site.register(Tarefa)

admin.site.register(MaterialQuantidade)

admin.site.register(Faculdade)

admin.site.register(Departamento)

admin.site.register(Sessao)

admin.site.register(SessaoAtividade)

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
