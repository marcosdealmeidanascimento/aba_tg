from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models.responsavel import Responsavel
from core.serializers import RegistroSerializer
from core.models.profissional import Profissional
from core.models import Usuario
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.serializers.responsavel_serializer import ResponsavelSerializer


class RegistroView(APIView):
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        if usuario.tipo_usuario == Usuario.USER_TYPE_CHOICES[0][0]:
            try:
                perfil = Profissional.objects.get(usuario=usuario)
                serializer = ProfissionalSerializer(perfil)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profissional.DoesNotExist:
                return Response(
                    {"error": "Perfil de profissional não encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif usuario.tipo_usuario == Usuario.USER_TYPE_CHOICES[1][0]:
            try:
                perfil = Responsavel.objects.get(usuario=usuario)
                serializer = ResponsavelSerializer(perfil)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Responsavel.DoesNotExist:
                return Response(
                    {"error": "Perfil de responsável não encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"error": "Tipo de usuário inválido."},
            status=status.HTTP_400_BAD_REQUEST
        )
