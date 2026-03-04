from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import PedidoVinculo
from core.serializers.pedido_vinculo_serializer import PedidoVinculoSerializer
from rest_framework.permissions import IsAuthenticated
from core.services.log_action import log_action


class PedidoVinculoViewSet(viewsets.ModelViewSet):
    queryset = PedidoVinculo.objects.all()
    serializer_class = PedidoVinculoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def responder(self, request, pk=None):
        pedido = self.get_object()
        novo_status = request.data.get('status') # 'aceito' ou 'recusado'
        pedido.status = novo_status
        pedido.save()

        if novo_status == 'aceito':
            pedido.paciente.profissionais.add(pedido.profissional)
            log_action(request.user, 'PEDIDO_VINCULO_ACEITO', f'Vínculo aceito. Paciente: {pedido.paciente.id}', request)
        else:
            log_action(request.user, 'PEDIDO_VINCULO_RECUSADO', f'Vínculo recusado. Paciente: {pedido.paciente.id}', request)

        return Response({"success": True})