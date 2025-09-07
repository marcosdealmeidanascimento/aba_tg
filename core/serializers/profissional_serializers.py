from rest_framework import serializers
from core.models import Profissional
from core.serializers.usuario_serializers import UsuarioSerializer


class ProfissionalSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'usuario_info',
            'licenca',
            'especialidade',
            'genero',
            'descricao',
            'telefone'
        ]
