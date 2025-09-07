from django.contrib import admin
from core.models import Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'licenca', 'especialidade', 'aprovado')
    search_fields = ('usuario__username', 'usuario__email', 'licenca')
    list_filter = ('especialidade', 'aprovado')
