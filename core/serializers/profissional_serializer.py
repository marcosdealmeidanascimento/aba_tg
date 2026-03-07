from rest_framework import serializers
from core.models import Profissional
from core.serializers.usuario_serializer import UsuarioSerializer


class ProfissionalSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'usuario_info',
            'foto_perfil',
            'arquivo_curriculo',
            'nome',
            'sobrenome',
            'registro_profissional',
            'especialidade_principal',
            'telefone_contato',
            'anos_experiencia_aba',
            'formacao_academica',
            'certificacoes',
            'bio_descricao',
            'genero',
        ]

    def get_foto_perfil_url(self, obj):
        """Opcional: Garante que a URL da foto venha completa do MinIO"""
        if obj.foto_perfil:
            return obj.foto_perfil.url
        return None
