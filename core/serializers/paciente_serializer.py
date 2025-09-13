from rest_framework import serializers
from core.models.paciente import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            'id',
            'nome',
            'data_nascimento',
            'descricao',
            'genero',
            'responsaveis',
            'profissionais',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['responsaveis', 'profissionais', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Cria o paciente com os dados validados
        paciente = Paciente.objects.create(**validated_data)

        # A instância do responsável será passada pela view
        responsavel_logado = self.context.get('responsavel_logado')

        if responsavel_logado:
            paciente.responsaveis.add(responsavel_logado)

        return paciente
