from rest_framework import serializers
from core.models.pedido_agendamento import PedidoAgendamento
from core.serializers.paciente_serializer import PacienteSerializer
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.responsavel_serializer import ResponsavelSerializer
from core.serializers.nivel_serializer import NivelSerializer
from core.serializers.disponibilidade_serializer import DisponibilidadeSerializer


class PedidoAgendamentoSerializer(serializers.ModelSerializer):
    paciente_detalhes = PacienteSerializer(source='paciente', read_only=True)
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)
    responsavel_detalhes = ResponsavelSerializer(source='responsavel', read_only=True)
    nivel_detalhes = NivelSerializer(source='nivel', read_only=True)
    disponibilidade_detalhes = DisponibilidadeSerializer(source='disponibilidade', read_only=True)
    duracao_estimada = serializers.SerializerMethodField()

    class Meta:
        model = PedidoAgendamento
        fields = [
            'id',
            'paciente', 'paciente_detalhes',
            'responsavel', 'responsavel_detalhes',
            'profissional', 'profissional_detalhes',
            'nivel', 'nivel_detalhes',
            'disponibilidade', 'disponibilidade_detalhes',
            'data_horario_proposta',
            'data_horario_fim_proposta',
            'duracao_estimada',
            'observacoes',
            'status',
            'motivo_recusa',
            'data_pedido',
            'sessao_criada',
        ]
        read_only_fields = [
            'status', 'motivo_recusa', 'data_pedido', 'sessao_criada', 'responsavel',
        ]

    def get_duracao_estimada(self, obj):
        if obj.data_horario_proposta and obj.data_horario_fim_proposta:
            delta = obj.data_horario_fim_proposta - obj.data_horario_proposta
            return int(delta.total_seconds() // 60)
        return None


class RecusarAgendamentoSerializer(serializers.Serializer):
    motivo_recusa = serializers.CharField()
