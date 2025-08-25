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

class IsResponsavelOwner(BasePermission):
    """
    Permite acesso apenas a responsáveis que são donos do objeto (ex: seu próprio paciente).
    """
    def has_object_permission(self, request, view, obj):
        # Neste caso, a lógica de checagem deve ser implementada na view.
        # Por exemplo: `obj.responsavel == request.user.responsavel`
        return False # Lógica será implementada depois