from core.models import Modulo
from rest_framework import serializers
from core.serializers.nivel_serializer import NivelSerializer


class ModuloSerializer(serializers.ModelSerializer):
    niveis = NivelSerializer(many=True, read_only=True)

    class Meta:
        model = Modulo
        fields = '__all__'
