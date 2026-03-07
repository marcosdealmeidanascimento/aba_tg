from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models.auditoria import AuditLog
from core.serializers.auditoria_serializer import AuditLogSerializer


class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AuditLog.objects.filter(usuario=self.request.user).order_by('-data_hora')
