from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from core.models import Diagnostico
from core.models.paciente import Paciente
from core.permissions import IsRelatedToPaciente
from core.serializers.diagnostico_serializer import DiagnosticoSerializer


class DiagnosticoViewSet(viewsets.ModelViewSet):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
    permission_classes = [IsAuthenticated, IsRelatedToPaciente]

    def get_queryset(self):
        user = self.request.user

        # Filtra os diagnósticos com base no tipo de usuário
        if hasattr(user, 'profissional'):
            # Profissional vê todos os diagnósticos dos seus pacientes
            return Diagnostico.objects.filter(
                paciente__in=user.profissional.pacientes_atendidos.all()
            )

        if hasattr(user, 'responsavel'):
            # Responsável vê todos os diagnósticos dos seus pacientes
            return Diagnostico.objects.filter(
                paciente__in=user.responsavel.pacientes_cuidados.all()
            )

        return Diagnostico.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Apenas profissionais podem criar diagnósticos
        if not hasattr(user, 'profissional'):
            raise PermissionDenied(
                "Apenas profissionais podem criar diagnósticos."
            )

        # Verifica se o paciente pertence ao profissional
        paciente = serializer.validated_data.get('paciente')
        if not user.profissional.pacientes_atendidos.filter(id=paciente.id).exists():
            raise PermissionDenied(
                "O paciente não pertence a este profissional."
            )

        # Associa o diagnóstico ao profissional logado
        serializer.context['profissional_logado'] = user.profissional
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user

        # Apenas o profissional que criou o diagnóstico pode editá-lo
        if not hasattr(user, 'profissional') or not user.profissional:
            raise PermissionDenied(
                "Você não tem permissão para editar este diagnóstico."
            )

        if not IsRelatedToPaciente().has_object_permission(self.request, self, serializer.instance.paciente):
            raise PermissionDenied(
                "Você não tem permissão para editar este diagnóstico."
            )

        serializer.instance.profissional = user.profissional
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        # Apenas o profissional que criou o diagnóstico pode deletá-lo
        if not hasattr(user, 'profissional') or not user.profissional:
            raise PermissionDenied(
                "Você não tem permissão para deletar este diagnóstico."
            )

        if not IsRelatedToPaciente().has_object_permission(self.request, self, instance.paciente):
            raise PermissionDenied(
                "Você não tem permissão para deletar este diagnóstico."
            )

        instance.delete()

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except Diagnostico.DoesNotExist:
            raise NotFound("Diagnóstico não encontrado.")


class GetDiagnosticoByPacienteView(generics.ListAPIView):
    serializer_class = DiagnosticoSerializer
    permission_classes = [IsAuthenticated, IsRelatedToPaciente]

    def get_queryset(self):
        # Acessa o ID do paciente a partir dos parâmetros da URL
        paciente_id = self.kwargs.get('paciente_id')

        # Busca o paciente para verificar se ele existe
        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            raise NotFound(f"Paciente com ID {paciente_id} não encontrado.")

        # Usa a permissão para verificar se o usuário logado tem acesso a este paciente
        if not IsRelatedToPaciente().has_object_permission(self.request, self, paciente):
            raise PermissionDenied("Você não tem permissão para acessar os diagnósticos deste paciente.")

        # Retorna o queryset filtrado
        return Diagnostico.objects.filter(paciente=paciente)