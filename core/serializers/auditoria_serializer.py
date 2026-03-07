from core.models.auditoria import AuditLog
from rest_framework import serializers
from core.serializers.usuario_serializer import UsuarioSerializer


class AuditLogSerializer(serializers.ModelSerializer):
    usuario_detalhes = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'usuario',
            'usuario_detalhes',
            'acao',
            'descricao',
            'ip_address',
            'user_agent',
            'data_hora'
        ]
