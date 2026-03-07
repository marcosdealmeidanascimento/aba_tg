from rest_framework import serializers
from core.models.execucao_atividade import ExecucaoAtividade
from core.serializers.atividade_serializer import AtividadeSerializer


class ExecucaoAtividadeSerializer(serializers.ModelSerializer):
    atividade_detalhes = AtividadeSerializer(source='atividade', read_only=True)

    class Meta:
        model = ExecucaoAtividade
        fields = [
            'id',
            'sessao',
            'atividade',
            'atividade_detalhes',
            'profissional',
            'paciente',
            'status',
            'notas',
            'created_at'
        ]
        read_only_fields = ['id', 'atividade_detalhes', 'created_at']
