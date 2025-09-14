from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Paciente, Profissional, Responsavel
from core.permissions import IsRelatedToPaciente
from core.serializers.paciente_serializer import PacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsRelatedToPaciente()]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profissional'):
            return user.profissional.pacientes_atendidos.all()
        if hasattr(user, 'responsavel'):
            return user.responsavel.pacientes_cuidados.all()
        return Paciente.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'responsavel'):
            raise PermissionDenied("Apenas responsáveis podem criar pacientes.")
        serializer.context['responsavel_logado'] = user.responsavel
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='vincular-profissional')
    def vincular_profissional(self, request, pk=None):
        paciente = Paciente.objects.get(id=pk)

        if not hasattr(request.user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem gerenciar vínculos.")

        profissional = request.user.profissional

        paciente.profissionais.add(profissional)
        return Response({"message": "Profissional vinculado com sucesso."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='desvincular-profissional')
    def desvincular_profissional(self, request, pk=None):
        paciente = Paciente.objects.get(id=pk)

        if not hasattr(request.user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem gerenciar vínculos.")

        profissional = request.user.profissional

        paciente.profissionais.remove(profissional)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='vincular-responsavel')
    def vincular_responsavel(self, request, pk=None):
        paciente = Paciente.objects.get(id=pk)
        
        if not hasattr(request.user, 'responsavel'):
            raise PermissionDenied("Apenas responsáveis podem gerenciar seus próprios vínculos.")

        responsavel = request.user.responsavel

        paciente.responsaveis.add(responsavel)
        return Response({"message": "Responsável vinculado com sucesso."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='desvincular-responsavel')
    def desvincular_responsavel(self, request, pk=None):
        paciente = Paciente.objects.get(id=pk)

        if not hasattr(request.user, 'responsavel'):
            raise PermissionDenied("Apenas responsáveis podem gerenciar seus próprios vínculos.")

        responsavel = request.user.responsavel

        paciente.responsaveis.remove(responsavel)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except Paciente.DoesNotExist:
            raise NotFound("Paciente não encontrado.")
