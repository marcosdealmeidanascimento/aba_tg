from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsResponsavel, IsResponsavelOwner
from core.models.responsavel import Responsavel
from core.serializers.responsavel_serializers import ResponsavelSerializer


class CompletarResponsavelView(APIView):
    permission_classes = [IsAuthenticated, IsResponsavel]

    def post(self, request):
        usuario = request.user

        if hasattr(usuario, 'responsavel'):
            return Response(
                {"error": "O perfil de responsável já existe. "
                 "Utilize a rota de atualização."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ResponsavelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=usuario)
            return Response(
                {"message": "Perfil de responsável completado com sucesso!"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResponsavelPerfilView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite visualizar, atualizar ou deletar
    o próprio perfil de responsável
    """
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticated, IsResponsavelOwner]
