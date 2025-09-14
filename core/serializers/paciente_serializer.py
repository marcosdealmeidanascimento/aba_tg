from rest_framework import serializers
from core.models import Paciente, Profissional, Responsavel
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.responsavel_serializer import ResponsavelSerializer


class PacienteSerializer(serializers.ModelSerializer):
    profissionais = ProfissionalSerializer(many=True, read_only=True)
    responsaveis = ResponsavelSerializer(many=True, read_only=True)

    class Meta:
        model = Paciente
        fields = [
            'id',
            'nome',
            'data_nascimento',
            'descricao',
            'genero',
            'profissionais',
            'responsaveis',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'profissionais', 'responsaveis', 'created_at', 'updated_at']

    def create(self, validated_data):
        paciente = Paciente.objects.create(**validated_data)
        responsavel_logado = self.context.get('responsavel_logado')
        if responsavel_logado:
            paciente.responsaveis.add(responsavel_logado)
        return paciente