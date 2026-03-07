from rest_framework import serializers
from core.models.atividade import Atividade
from core.serializers.nivel_serializer import NivelSerializer


class AtividadeSerializer(serializers.ModelSerializer):
    nivel_detalhes = NivelSerializer(source='nivel', read_only=True)

    class Meta:
        model = Atividade
        fields = [
            'id',
            'nome',
            'descricao',
            'categoria',
            'nivel',
            'nivel_detalhes',
        ]

        read_only_fields = ['id', 'nivel_detalhes']
