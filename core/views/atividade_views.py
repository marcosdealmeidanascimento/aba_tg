from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from core.models import Atividade
from core.serializers import AtividadeSerializer


class AtividadeViewSet(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer

    def get_queryset(self):
        queryset = Atividade.objects.all()
        nivel_id = self.request.query_params.get('nivelId', None)
        if nivel_id is not None:
            queryset = queryset.filter(nivel_id=nivel_id)
        return queryset