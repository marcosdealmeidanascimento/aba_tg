from rest_framework import serializers
from core.models.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    usuario = serializers.SerializerMethodField()
    respondido_por_nome = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id',
            'titulo',
            'mensagem',
            'usuario',
            'status',
            'data',
            'resposta',
            'data_resposta',
            'respondido_por_nome',
        ]
        read_only_fields = ['id', 'usuario', 'status', 'data', 'resposta', 'data_resposta', 'respondido_por_nome']

    def get_usuario(self, obj):
        u = obj.usuario
        nome = f"{getattr(u, 'first_name', '')} {getattr(u, 'last_name', '')}".strip()
        return nome or u.username

    def get_respondido_por_nome(self, obj):
        if not obj.respondido_por:
            return None
        u = obj.respondido_por
        nome = f"{getattr(u, 'first_name', '')} {getattr(u, 'last_name', '')}".strip()
        return nome or u.username


class ResponderTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['resposta']
