from rest_framework import serializers
from core.models import Sessao
from core.models.habilidade import Nivel
from core.serializers.paciente_serializer import PacienteSerializer
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.nivel_serializer import NivelSerializer
from core.models.paciente import Paciente
from django.utils import timezone


class SessaoSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all(), write_only=True, source='paciente')
    nivel = NivelSerializer(read_only=True)
    nivel_id = serializers.PrimaryKeyRelatedField(queryset=Nivel.objects.all(), write_only=True, source='nivel')
    profissional = ProfissionalSerializer(read_only=True)

    class Meta:
        model = Sessao
        fields = ['id', 'data_horario_inicio', 'data_horario_fim', 'data_horario_fim_prevista', 'paciente_id', 'paciente', 'observacoes', 'profissional', 'responsavel', 'nivel_id', 'nivel']
        read_only_fields = ['id', 'profissional', 'data_horario_inicio']

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.tipo_usuario == 'profissional':
            profissional = user.profissional
            validated_data['profissional'] = profissional
        elif user.tipo_usuario == 'responsavel':
            responsavel = user.responsavel
            validated_data['responsavel'] = responsavel

        return super().create(validated_data)


class FecharSessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessao
        fields = ['id', 'data_horario_fim', 'observacoes']

    def update(self, instance, validated_data):
        instance.data_horario_fim = timezone.now()
        instance.observacoes = validated_data.get('observacoes', instance.observacoes)
        instance.save()
        return instance
