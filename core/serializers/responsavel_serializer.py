from rest_framework import serializers
from core.models import Responsavel
from core.serializers.usuario_serializer import UsuarioSerializer


class ResponsavelSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Responsavel
        fields = [
            'usuario_info',
            'foto_perfil',
            'nome',
            'sobrenome',
            'parentesco',
            'genero',
            'telefone',
            'cpf',
            'endereco'
        ]

    def get_foto_perfil_url(self, obj):
        if obj.foto_perfil:
            return obj.foto_perfil.url
        return None
