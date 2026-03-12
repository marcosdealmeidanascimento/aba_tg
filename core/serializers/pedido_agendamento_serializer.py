from rest_framework import serializers
from core.models.pedido_agendamento import PedidoAgendamento
from core.serializers.paciente_serializer import PacienteSerializer
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.responsavel_serializer import ResponsavelSerializer
from core.serializers.nivel_serializer import NivelSerializer


class PedidoAgendamentoSerializer(serializers.ModelSerializer):
    paciente_detalhes = PacienteSerializer(source='paciente', read_only=True)
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)
    responsavel_detalhes = ResponsavelSerializer(source='responsavel', read_only=True)
    nivel_detalhes = NivelSerializer(source='nivel', read_only=True)

    class Meta:
        model = PedidoAgendamento
        fields = [
            'id',
            'paciente', 'paciente_detalhes',
            'responsavel', 'responsavel_detalhes',
            'profissional', 'profissional_detalhes',
            'nivel', 'nivel_detalhes',
            'data_horario_proposta',
            'observacoes',
            'status',
            'motivo_recusa',
            'data_pedido',
            'sessao_criada',
        ]
        read_only_fields = ['status', 'motivo_recusa', 'data_pedido', 'sessao_criada', 'responsavel']


class RecusarAgendamentoSerializer(serializers.Serializer):
    motivo_recusa = serializers.CharField()
