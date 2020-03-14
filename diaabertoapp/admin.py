from django.contrib import admin
from diaabertoapp.models import Edificio, Campus, LocalAtividade, Tematica, Atividade, Material, MaterialQuantidade
from django.utils.safestring import mark_safe

# Register your models here.

class CampusAdmin(admin.ModelAdmin):
    list_display = ('nome', 'morada', 'contacto')

admin.site.register(Campus, CampusAdmin)

class LocalAtividadeAdmin(admin.ModelAdmin):
    list_display = ('sala','andar', 'get_edificio', 'descricao', 'get_campus')

    def get_campus(self, obj):
        return obj.edificio.campus.nome
    get_campus.short_description = "Campus"
    def get_edificio(self, obj):
        return obj.edificio.nome
    get_edificio.short_description = "Edificio"

admin.site.register(LocalAtividade, LocalAtividadeAdmin)
admin.site.register(Tematica)
admin.site.register(Material)
admin.site.register(MaterialQuantidade)

class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'campus')

admin.site.register(Edificio, EdificioAdmin)

class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'local', 'duracao', 'limite_participantes', 'tipo_atividade', 'publico_alvo', 'colored_name')
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
