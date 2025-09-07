from rest_framework import serializers
from core.models import Responsavel
from core.serializers.usuario_serializers import UsuarioSerializer


class ResponsavelSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Responsavel
        fields = [
            'usuario_info',
            'parentesco',
            'genero'
        ]
