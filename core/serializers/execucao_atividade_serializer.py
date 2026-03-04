from rest_framework import serializers
from core.models.execucao_atividade import ExecucaoAtividade


class ExecucaoAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecucaoAtividade
        fields = '__all__'
