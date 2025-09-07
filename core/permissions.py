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


class IsProfissionalOrResponsavel(BasePermission):
    """
    Permite acesso apenas a pacientes que são atendidos por um profissional ou
    cadastrados por um responsável.
    """
    def has_permission(self, request, view):
        # Permite a visualização da lista se o
        # usuário for profissional ou responsável
        if not hasattr(request.user, 'profissional') and \
           not hasattr(request.user, 'responsavel'):
            return False
        return True


class IsRelatedToPaciente(BasePermission):
    """
    Permite acesso apenas se o usuário logado for um dos profissionais ou 
    responsáveis relacionados ao paciente.
    """
    def has_object_permission(self, request, view, obj):
        # Verifica se o usuário é um profissional
        # e se está relacionado ao paciente
        if hasattr(request.user, 'profissional'):
            return request.user.profissional in obj.profissionais.all()

        # Verifica se o usuário é um responsável
        # e se está relacionado ao paciente
        if hasattr(request.user, 'responsavel'):
            return request.user.responsavel in obj.responsaveis.all()

        return False