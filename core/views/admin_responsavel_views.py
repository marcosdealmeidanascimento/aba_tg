from rest_framework import generics
from core.models.responsavel import Responsavel
from core.permissions import IsAdmin
from core.serializers.responsavel_serializer import ResponsavelSerializer


class AdminResponsavelListView(generics.ListAPIView):
    """
    GET /api/admin/responsaveis/
    Lista todos os responsáveis cadastrados. Requer admin.
    """
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = Responsavel.objects.select_related('usuario').all().order_by('nome')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(nome__icontains=q) | qs.filter(sobrenome__icontains=q)
        return qs
