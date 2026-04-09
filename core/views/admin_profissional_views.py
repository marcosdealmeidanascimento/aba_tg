from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models.profissional import Profissional
from core.permissions import IsAdmin
from core.serializers.admin_profissional_serializer import (
    AdminProfissionalListSerializer,
    AdminProfissionalDetailSerializer,
    ValidacaoProfissionalSerializer,
)
from core.services.log_action import log_action


class AdminProfissionalListView(generics.ListAPIView):
    """
    GET /api/admin/profissionais/
    Lista todos os profissionais. Filtros: status, especialidade, cidade.
    """
    serializer_class = AdminProfissionalListSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = Profissional.objects.select_related('usuario').all()
        p = self.request.query_params

        if status_val := p.get('status'):
            qs = qs.filter(status_validacao=status_val)

        if especialidade := p.get('especialidade'):
            qs = qs.filter(especialidade_principal__icontains=especialidade)

        if cidade := p.get('cidade'):
            qs = qs.filter(atendimento_cidade__icontains=cidade)

        allowed_orderings = {
            'nome': 'nome',
            '-nome': '-nome',
            'recente': '-data_cadastro',
            '-recente': 'data_cadastro',
            'status': 'status_validacao',
        }
        ordering = p.get('ordering', 'recente')
        return qs.order_by(allowed_orderings.get(ordering, '-data_cadastro'))


class AdminProfissionalDetailView(generics.RetrieveAPIView):
    """
    GET /api/admin/profissionais/<pk>/
    Detalhe completo de um profissional incluindo arquivos.
    """
    queryset = Profissional.objects.select_related('usuario').all()
    serializer_class = AdminProfissionalDetailSerializer
    permission_classes = [IsAdmin]


class AdminValidacaoProfissionalView(APIView):
    """
    PATCH /api/admin/profissionais/<pk>/validacao/
    Atualiza campos de validação e registra no audit log.
    """
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            profissional = Profissional.objects.get(pk=pk)
        except Profissional.DoesNotExist:
            return Response(
                {"detail": "Profissional não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        status_anterior = profissional.status_validacao

        serializer = ValidacaoProfissionalSerializer(
            profissional, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        status_novo = profissional.status_validacao
        log_action(
            user=request.user,
            acao='Validou profissional',
            descricao=(
                f"Admin atualizou validação do profissional ID={pk} "
                f"({profissional.nome} {profissional.sobrenome}). "
                f"Status: {status_anterior} → {status_novo}."
            ),
            request=request,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
