from django.contrib import admin
from diaabertoapp.models import Edificio, Campus, LocalAtividade, Atividade

# Register your models here.
admin.site.register(Edificio)
admin.site.register(Campus)
admin.site.register(LocalAtividade)
admin.site.register(Atividade)