from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'tipo_usuario')
    search_fields = ('username', 'email')
    list_filter = ('tipo_usuario',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais',
         {'fields': ('email', 'first_name', 'last_name')}),
        ('Tipo de Usuário', {'fields': ('tipo_usuario',)}),
    )

    ordering = ('username',)
