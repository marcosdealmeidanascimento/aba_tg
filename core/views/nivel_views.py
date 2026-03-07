from rest_framework import viewsets
from core.models import Nivel
from core.serializers import NivelSerializer


class NivelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer
