from rest_framework import serializers
from core.models.pedido_vinculo import PedidoVinculo
from core.serializers.paciente_serializer import PacienteSerializer
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.responsavel_serializer import ResponsavelSerializer


class PedidoVinculoSerializer(serializers.ModelSerializer):
    paciente_detalhes = PacienteSerializer(source='paciente', read_only=True)
    responsavel_detalhes = ResponsavelSerializer(source='responsavel', read_only=True)
    profissional_detalhes = ProfissionalSerializer(source='profissional', read_only=True)

    class Meta:
        model = PedidoVinculo
        fields = [
            'id',
            'paciente', 'paciente_detalhes',
            'responsavel', 'responsavel_detalhes',
            'profissional', 'profissional_detalhes',
            'status'
        ]
