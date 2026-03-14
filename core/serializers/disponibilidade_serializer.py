from rest_framework import serializers
from core.models.disponibilidade_profissional import DisponibilidadeProfissional


class DisponibilidadeSerializer(serializers.ModelSerializer):
    ocupado = serializers.SerializerMethodField()

    class Meta:
        model = DisponibilidadeProfissional
        fields = [
            'id',
            'profissional',
            'data_horario_inicio',
            'data_horario_fim',
            'recorrente',
            'dia_semana',
            'ativo',
            'ocupado',
        ]
        read_only_fields = ['id', 'profissional', 'ocupado']

    def get_ocupado(self, obj):
        return obj.is_ocupado()

    def validate(self, data):
        if data.get('recorrente') and data.get('dia_semana') is None:
            raise serializers.ValidationError(
                {'dia_semana': 'dia_semana é obrigatório para slots recorrentes.'}
            )
        inicio = data.get('data_horario_inicio')
        fim = data.get('data_horario_fim')
        if inicio and fim and fim <= inicio:
            raise serializers.ValidationError(
                {'data_horario_fim': 'O horário de fim deve ser posterior ao de início.'}
            )
        return data
