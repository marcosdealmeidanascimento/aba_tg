from rest_framework import serializers
from core.models import Profissional
from core.serializers.usuario_serializer import UsuarioSerializer


class ProfissionalSerializer(serializers.ModelSerializer):
    # Mantendo a info do usuário (geralmente e-mail/username) como leitura
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'usuario_info',
            # Novos campos de Upload (MinIO/S3)
            'foto_perfil',
            'arquivo_curriculo',
            # Dados Básicos (conforme a imagem)
            'nome',
            'sobrenome',
            'registro_profissional', # (CRP/CRM/etc)
            'especialidade_principal',
            'telefone_contato',
            'anos_experiencia_aba',
            # Formação e Qualificações (conforme a imagem)
            'formacao_academica',
            'certificacoes',
            'bio_descricao',
            # Campos que você já tinha (ajuste se mudou o nome no Model)
            'genero',
        ]

    def get_foto_perfil_url(self, obj):
        """Opcional: Garante que a URL da foto venha completa do MinIO"""
        if obj.foto_perfil:
            return obj.foto_perfil.url
        return None
