from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models.profissional import Profissional
from core.permissions import IsProfissional, IsProfissionalOwner
from core.serializers.profissional_serializers import ProfissionalSerializer


class CompletarProfissionalView(APIView):
    permission_classes = [IsAuthenticated, IsProfissional]

    def post(self, request):
        usuario = request.user
        if hasattr(usuario, 'profissional'):
            return Response(
                {"error": "O perfil profissional já existe. "
                 "Utilize a rota de atualização."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfissionalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(usuario=usuario) 
            message = "Perfil profissional completado com sucesso!"
            return Response(
                {"message": message},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfissionalPerfilView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite visualizar, atualizar ou deletar
    o próprio perfil de profissional.
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated, IsProfissionalOwner]
