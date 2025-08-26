from rest_framework import serializers
from core.models import Usuario, Profissional, Responsavel

class RegistroSerializer(serializers.ModelSerializer):
    tipo_usuario = serializers.ChoiceField(
        choices=Usuario.USER_TYPE_CHOICES, 
        write_only=True
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(**validated_data)

        return usuario