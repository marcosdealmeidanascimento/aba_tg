from rest_framework import viewsets
from core.models import Modulo
from core.serializers import ModuloSerializer


class ModuloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modulo.objects.all()
    serializer_class = ModuloSerializer
