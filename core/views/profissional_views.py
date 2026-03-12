from django.db import models
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


class ProfissionalListView(generics.ListAPIView):
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Profissional.objects.all()
        p = self.request.query_params

        # Busca textual geral: nome, sobrenome, especialidade, bio, certificações
        search = p.get('search')
        if search:
            qs = qs.filter(
                models.Q(nome__icontains=search)
                | models.Q(sobrenome__icontains=search)
                | models.Q(especialidade_principal__icontains=search)
                | models.Q(bio_descricao__icontains=search)
                | models.Q(certificacoes__icontains=search)
                | models.Q(formacao_academica__icontains=search)
            )

        # Filtros individuais
        if especialidade := p.get('especialidade'):
            qs = qs.filter(especialidade_principal__icontains=especialidade)

        if certificacao := p.get('certificacao'):
            qs = qs.filter(certificacoes__icontains=certificacao)

        if genero := p.get('genero'):
            qs = qs.filter(genero__iexact=genero)

        if cidade := p.get('cidade'):
            qs = qs.filter(atendimento_cidade__icontains=cidade)

        if uf := p.get('uf'):
            qs = qs.filter(atendimento_uf__iexact=uf)

        if bairro := p.get('bairro'):
            qs = qs.filter(atendimento_bairro__icontains=bairro)

        # Experiência mínima e máxima
        if exp_min := p.get('exp_min'):
            qs = qs.filter(anos_experiencia_aba__gte=exp_min)

        if exp_max := p.get('exp_max'):
            qs = qs.filter(anos_experiencia_aba__lte=exp_max)

        # Ordenação
        ordering = p.get('ordering', 'nome')
        allowed_orderings = {
            'nome': 'nome',
            '-nome': '-nome',
            'exp': 'anos_experiencia_aba',
            '-exp': '-anos_experiencia_aba',
            'recente': '-data_cadastro',
        }
        qs = qs.order_by(allowed_orderings.get(ordering, 'nome'))

        return qs


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
