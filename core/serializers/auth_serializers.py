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
        # Garante que a senha é removida dos dados validados
        password = validated_data.pop('password')
        tipo_usuario = validated_data.pop('tipo_usuario')

        # Cria o objeto de usuário de forma segura
        usuario = Usuario.objects.create_user(password=password, **validated_data)

        if tipo_usuario == 'profissional':
            Profissional.objects.create(usuario=usuario)
        else:
            Responsavel.objects.create(usuario=usuario)

        return usuario