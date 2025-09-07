from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Usuario
from core.serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
