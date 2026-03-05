from django.contrib import admin
from core.models import Responsavel


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    pass