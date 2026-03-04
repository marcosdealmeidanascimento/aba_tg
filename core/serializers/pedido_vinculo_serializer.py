from rest_framework import serializers
from core.models.pedido_vinculo import PedidoVinculo


class PedidoVinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoVinculo
        fields = '__all__'
