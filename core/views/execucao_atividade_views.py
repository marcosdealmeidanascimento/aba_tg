from rest_framework import viewsets
from core.models import ExecucaoAtividade
from core.serializers.execucao_atividade_serializer import ExecucaoAtividadeSerializer


class ExecucaoAtividadeViewSet(viewsets.ModelViewSet):
    queryset = ExecucaoAtividade.objects.all()
    serializer_class = ExecucaoAtividadeSerializer
