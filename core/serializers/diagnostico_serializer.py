from rest_framework import serializers
from core.models import Diagnostico
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.models import Paciente


class DiagnosticoSerializer(serializers.ModelSerializer):
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    profissional = ProfissionalSerializer(read_only=True)

    class Meta:
        model = Diagnostico
        fields = [
            'id',
            'paciente',
            'nivel',
            'observacoes',
            'profissional',
            'data_diagnostico'
        ]
        read_only_fields = ['profissional', 'data_diagnostico', 'paciente']

    def create(self, validated_data):
        diagnostico = Diagnostico.objects.create(**validated_data)
        profissional_logado = self.context.get('profissional_logado')
        diagnostico.profissional = profissional_logado
        diagnostico.save()
        return diagnostico
