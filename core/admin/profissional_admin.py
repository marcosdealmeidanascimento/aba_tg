from django.contrib import admin
from core.models import Profissional


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    pass
