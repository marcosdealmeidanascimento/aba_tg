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
            'criado_em',
        ]
        read_only_fields = ['responsaveis', 'profissionais', 'criado_em']

    def create(self, validated_data):
        # Cria o paciente com os dados validados
        paciente = Paciente.objects.create(**validated_data)

        # A instância do responsável será passada pela view
        responsavel_logado = self.context.get('responsavel_logado')

        # A instância do profissional será passada pela view
        profissional_logado = self.context.get('profissional_logado')

        if responsavel_logado:
            paciente.responsaveis.add(responsavel_logado)

        if profissional_logado:
            paciente.profissionais.add(profissional_logado)

        return paciente
