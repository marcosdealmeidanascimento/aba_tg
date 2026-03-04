from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Sessao, Paciente
from core.serializers.sessao_serializer import FecharSessaoSerializer, SessaoSerializer
from core.permissions import IsProfissional, IsRelatedToPaciente
from django.core.exceptions import ObjectDoesNotExist

from core.services.log_action import log_action

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
        paciente = serializer.validated_data.get('paciente')

        try:
            responsavel = user.responsavel
            if responsavel.pacientes_cuidados.filter(id=paciente.id).exists():
                serializer.save(responsavel=responsavel)
                return
        except ObjectDoesNotExist:
            pass

        try:
            profissional = user.profissional
            if profissional.pacientes_atendidos.filter(id=paciente.id).exists():
                serializer.save(profissional=profissional)
                log_action(user=user, acao='criou_sessao', descricao='Sessão criada com sucesso!', request=self.request)
                return
        except ObjectDoesNotExist:
            pass

        raise PermissionDenied(
            "Apenas pacientes vinculados ao profissional ou responsável podem criar sessões."
        )


class FecharSessaoAPIView(APIView):
    queryset = Sessao.objects.all()
    serializer_class = FecharSessaoSerializer
    permission_classes = [IsAuthenticated, IsRelatedToPaciente]

    def post(self, request, pk):
        user = self.request.user

        sessao = Sessao.objects.get(pk=pk)
        serializer = FecharSessaoSerializer(sessao, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data_horario_fim=timezone.now())
        if hasattr(user, 'profissional'):
            log_action(user=user, acao='fechar_sessao', descricao='Sessão fechada com sucesso!', request=self.request)

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

        if hasattr(user, 'profissional'):
            log_action(user, 'visualizou', 'sessoes', self.request)
            return Sessao.objects.filter(paciente=paciente, profissional=user.profissional)
        elif hasattr(user, 'responsavel'):
            return Sessao.objects.filter(paciente=paciente, responsavel=user.responsavel)

        return Sessao.objects.none()
