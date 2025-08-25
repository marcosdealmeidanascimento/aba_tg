from rest_framework import serializers
from core.models import Responsavel

class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ['nome_da_crianca', 'parentesco']