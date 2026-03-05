from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.responsavel import Responsavel
from core.permissions import IsResponsavelOwner
from rest_framework.permissions import IsAuthenticated
from core.serializers.responsavel_serializer import ResponsavelSerializer
from core.services.log_action import log_action


class CompletarResponsavelView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        usuario = request.user
        if hasattr(usuario, 'responsavel'):
            return Response(
                {"error": "O perfil de responsável já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ResponsavelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=usuario)
            log_action(user=usuario, acao='Criou perfil de responsável', descricao='Perfil de responsável criado com sucesso!', request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Permite atualizar o perfil sem enviar todos os campos"""
        try:
            responsavel = request.user.responsavel
        except Responsavel.DoesNotExist:
            return Response({"error": "Perfil não encontrado."}, status=404)

        serializer = ResponsavelSerializer(responsavel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ResponsavelPerfilView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticated, IsResponsavelOwner]
    parser_classes = [MultiPartParser, FormParser]
