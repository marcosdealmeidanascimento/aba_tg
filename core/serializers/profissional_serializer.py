from rest_framework import serializers
from core.models import Profissional
from core.serializers.usuario_serializer import UsuarioSerializer


class ProfissionalSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioSerializer(source='usuario', read_only=True)
    id = serializers.IntegerField(source='usuario_id', read_only=True)

    class Meta:
        model = Profissional
        fields = [
            'id',
            'usuario_info',
            'foto_perfil',
            'arquivo_curriculo',
            'nome',
            'sobrenome',
            'genero',
            'registro_profissional',
            'especialidade_principal',
            'anos_experiencia_aba',
            'formacao_academica',
            'certificacoes',
            'bio_descricao',
            'atendimento_cidade',
            'atendimento_uf',
            'atendimento_bairro',
            'atendimento_logradouro',
            'atendimento_numero',
            'atendimento_complemento',
            'atendimento_cep',
            'telefone_contato',
            'email_contato',
            'data_cadastro',
        ]
