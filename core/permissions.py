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
    Admin tem acesso a qualquer perfil.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.tipo_usuario == 'admin':
            return True
        return obj.usuario == request.user


class IsResponsavelOwner(BasePermission):
    """
    Permite acesso apenas se o usuário for o dono do perfil de responsável.
    Admin tem acesso a qualquer perfil.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.tipo_usuario == 'admin':
            return True
        return obj.usuario == request.user


class IsProfissionalOrResponsavel(BasePermission):
    """
    Permite acesso apenas a pacientes que são atendidos por um profissional ou
    cadastrados por um responsável. Admin tem acesso irrestrito.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.tipo_usuario == 'admin':
            return True
        if not hasattr(request.user, 'profissional') and \
           not hasattr(request.user, 'responsavel'):
            return False
        return True


class IsRelatedToPaciente(BasePermission):
    """
    Permite acesso apenas se o usuário logado for um dos profissionais ou
    responsáveis relacionados ao paciente da sessão. Admin tem acesso irrestrito.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.tipo_usuario == 'admin':
            return True

        paciente_instance = obj.paciente

        if hasattr(request.user, 'profissional'):
            return paciente_instance in request.user.profissional.pacientes_atendidos.all()

        if hasattr(request.user, 'responsavel'):
            return paciente_instance in request.user.responsavel.pacientes_cuidados.all()

        return False


class IsAdmin(BasePermission):
    """
    Permite acesso apenas a usuários com tipo_usuario 'admin'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'admin'
