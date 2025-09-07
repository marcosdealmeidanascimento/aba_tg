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


class IsProfissionalOwner(BasePermission):
    """
    Permite acesso apenas se o usuário for o dono do perfil profissional.
    """
    def has_object_permission(self, request, view, obj):
        # obj é a instância do objeto (neste caso, o perfil de Profissional)
        return obj.usuario == request.user


class IsResponsavelOwner(BasePermission):
    """
    Permite acesso apenas se o usuário for o dono do perfil de responsável.
    """
    def has_object_permission(self, request, view, obj):
        # obj é a instância do objeto (neste caso, o perfil de Responsável)
        return obj.usuario == request.user
