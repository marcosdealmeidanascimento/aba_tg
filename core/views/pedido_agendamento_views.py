from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import PedidoAgendamento, Sessao
from core.models.disponibilidade_profissional import DisponibilidadeProfissional
from core.serializers.pedido_agendamento_serializer import (
    PedidoAgendamentoSerializer,
    RecusarAgendamentoSerializer,
)
from core.permissions import IsResponsavel, IsProfissional
from core.services.log_action import log_action


class PedidoAgendamentoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoAgendamentoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profissional'):
            return PedidoAgendamento.objects.filter(profissional=user.profissional).order_by('-data_pedido')
        if hasattr(user, 'responsavel'):
            return PedidoAgendamento.objects.filter(responsavel=user.responsavel).order_by('-data_pedido')
        return PedidoAgendamento.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'responsavel'):
            raise PermissionDenied("Apenas responsáveis podem criar pedidos de agendamento.")

        responsavel = user.responsavel
        paciente = serializer.validated_data.get('paciente')
        profissional = serializer.validated_data.get('profissional')

        if not responsavel.pacientes_cuidados.filter(id=paciente.id).exists():
            raise PermissionDenied("Você não está vinculado a este paciente.")

        if not profissional.pacientes_atendidos.filter(id=paciente.id).exists():
            raise ValidationError("O profissional selecionado não atende este paciente.")

        disponibilidade = serializer.validated_data.get('disponibilidade')
        extra = {}

        if disponibilidade:
            if disponibilidade.profissional != profissional:
                raise ValidationError("O slot de disponibilidade não pertence ao profissional selecionado.")
            if disponibilidade.is_ocupado():
                raise ValidationError("Slot já reservado.")
            extra['data_horario_proposta'] = disponibilidade.data_horario_inicio
            extra['data_horario_fim_proposta'] = disponibilidade.data_horario_fim
        else:
            inicio = serializer.validated_data.get('data_horario_proposta')
            fim = serializer.validated_data.get('data_horario_fim_proposta')
            if inicio and fim and fim <= inicio:
                raise ValidationError("data_horario_fim_proposta deve ser posterior a data_horario_proposta.")

        pedido = serializer.save(responsavel=responsavel, **extra)
        log_action(
            user=user,
            acao='Pedido de Agendamento',
            descricao=f'Pedido de agendamento criado para paciente {paciente.id}',
            request=self.request,
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsProfissional])
    def aceitar(self, request, pk=None):
        pedido = self.get_object()
        user = request.user

        if pedido.profissional != user.profissional:
            raise PermissionDenied("Você não é o profissional responsável por este pedido.")

        if pedido.status != 'pendente':
            raise ValidationError("Este pedido já foi respondido.")

        sessao = Sessao.objects.create(
            paciente=pedido.paciente,
            profissional=pedido.profissional,
            nivel=pedido.nivel,
            data_horario_inicio=pedido.data_horario_proposta,
            data_horario_fim_prevista=pedido.data_horario_fim_proposta,
            observacoes=pedido.observacoes,
        )

        pedido.status = 'aceito'
        pedido.sessao_criada = sessao
        pedido.save()

        log_action(
            user=user,
            acao='Agendamento Aceito',
            descricao=f'Pedido {pedido.id} aceito. Sessão {sessao.id} criada.',
            request=request,
        )

        return Response(PedidoAgendamentoSerializer(pedido).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsProfissional])
    def recusar(self, request, pk=None):
        pedido = self.get_object()
        user = request.user

        if pedido.profissional != user.profissional:
            raise PermissionDenied("Você não é o profissional responsável por este pedido.")

        if pedido.status != 'pendente':
            raise ValidationError("Este pedido já foi respondido.")

        serializer = RecusarAgendamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pedido.status = 'recusado'
        pedido.motivo_recusa = serializer.validated_data['motivo_recusa']
        pedido.save()

        log_action(
            user=user,
            acao='Agendamento Recusado',
            descricao=f'Pedido {pedido.id} recusado. Motivo: {pedido.motivo_recusa}',
            request=request,
        )

        return Response(PedidoAgendamentoSerializer(pedido).data)
