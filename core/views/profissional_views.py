from rest_framework import status, viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models.profissional import Profissional
from core.permissions import IsProfissional, IsProfissionalOwner
from rest_framework.parsers import MultiPartParser, FormParser
from core.serializers.profissional_serializer import ProfissionalSerializer
from core.services.log_action import log_action


class ProfissionalListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profissionais = Profissional.objects.all()
        serializer = ProfissionalSerializer(profissionais, many=True)
        return Response(serializer.data)


class CompletarProfissionalView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        try:
            return Profissional.objects.get(usuario=self.request.user)
        except Profissional.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        profissional = self.get_object()

        if not profissional:
            return Response({"detail": "Perfil não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfissionalSerializer(profissional, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            log_action(user=request.user, acao='Atualizou perfil de profissional', descricao='Perfil de profissional atualizado com sucesso!', request=request)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = ProfissionalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            log_action(user=request.user, acao='Criou perfil de profissional', descricao='Perfil de profissional criado com sucesso!', request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfissionalPerfilView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permite visualizar, atualizar ou deletar
    o próprio perfil de profissional.
    """
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated, IsProfissionalOwner]
    parser_classes = [MultiPartParser, FormParser]
