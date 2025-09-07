from rest_framework.permissions import BasePermission


class IsProfissional(BasePermission):
    """
    Permite acesso apenas a usuários que são profissionais.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'profissional'


class IsResponsavel(BasePermission):
    """
    Permite acesso apenas a usuários que são responsáveis.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'responsavel'
