from rest_framework import serializers
from core.models import Profissional


class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = [
            'licenca', 
            'especialidade', 
            'genero', 
            'descricao', 
            'telefone'
        ]
