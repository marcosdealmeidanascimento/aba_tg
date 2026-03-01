from rest_framework import serializers
from core.models import Usuario


class RegistroSerializer(serializers.ModelSerializer):
    tipo_usuario = serializers.ChoiceField(
        choices=Usuario.USER_TYPE_CHOICES, 
        write_only=True,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        usuario = Usuario.objects.create_user(**validated_data)

        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
