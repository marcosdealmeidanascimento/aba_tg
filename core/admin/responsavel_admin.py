from django.contrib import admin
from core.models import Responsavel


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'parentesco')
    search_fields = ('usuario__username', 'usuario__email')
    list_filter = ('parentesco',)
