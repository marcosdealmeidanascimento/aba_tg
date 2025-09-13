from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Sessao, Paciente
from core.serializers.sessao_serializer import FecharSessaoSerializer, SessaoSerializer
from core.permissions import IsProfissional, IsRelatedToPaciente


class SessaoViewSet(viewsets.ModelViewSet):
    queryset = Sessao.objects.all()
    serializer_class = SessaoSerializer
    permission_classes = [IsAuthenticated, IsRelatedToPaciente]

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'profissional'):
            return Sessao.objects.filter(profissional=user.profissional)
        if hasattr(user, 'responsavel'):
            return Sessao.objects.filter(paciente__in=user.responsavel.pacientes_cuidados.all())
        return Sessao.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem criar sessões.")

        paciente = serializer.validated_data.get('paciente')
        if not user.profissional.pacientes_atendidos.filter(id=paciente.id).exists():
            raise PermissionDenied("Você não tem permissão para criar sessões para este paciente.")
        
        serializer.save(profissional=user.profissional)


class FecharSessaoAPIView(APIView):
    queryset = Sessao.objects.all()
    serializer_class = FecharSessaoSerializer
    permission_classes = [IsAuthenticated, IsRelatedToPaciente]

    def post(self, request, pk):
        user = self.request.user

        if not hasattr(user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem fechar sessões.")

        sessao = Sessao.objects.get(pk=pk)
        serializer = FecharSessaoSerializer(sessao, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data_horario_fim=timezone.now())

        return Response(serializer.data)


class GetSessoesByPacienteView(generics.ListAPIView):
    serializer_class = SessaoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        paciente_id = self.kwargs.get('paciente_id')

        try:
            paciente = Paciente.objects.get(id=paciente_id)
        except Paciente.DoesNotExist:
            raise NotFound("Paciente não encontrado.")

        if hasattr(user, 'profissional'):
            if paciente not in user.profissional.pacientes_atendidos.all():
                raise PermissionDenied("Você não tem permissão para acessar as sessões deste paciente.")
        elif hasattr(user, 'responsavel'):
            if paciente not in user.responsavel.pacientes_cuidados.all():
                raise PermissionDenied("Você não tem permissão para acessar as sessões deste paciente.")
        else:
            raise PermissionDenied("Você não tem permissão para acessar as sessões deste paciente.")

        return Sessao.objects.filter(paciente=paciente)