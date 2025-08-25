from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers import RegistroSerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsProfissional

class RegistroView(APIView):
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DadosProfissionalView(APIView):
    permission_classes = [IsAuthenticated, IsProfissional]

    def get(self, request):
        return Response({"message": "Olá, profissional! Você tem acesso a este conteúdo."})
