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

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profissional'):
            return PedidoVinculo.objects.filter(profissional=user.profissional, status='pendente')
        elif hasattr(user, 'responsavel'):
            return PedidoVinculo.objects.filter(paciente__in=user.responsavel.pacientes_cuidados.all()).order_by('-id')
        return PedidoVinculo.objects.none()

    @action(detail=True, methods=['post'])
    def responder(self, request, pk=None):
        pedido = self.get_object()
        novo_status = request.data.get('status') # 'aceito' ou 'recusado'
        pedido.status = novo_status
        pedido.save()

        if novo_status == 'aceito':
            pedido.paciente.profissionais.add(pedido.profissional)
            log_action(request.user, 'Pedido aceito', f'Vínculo aceito. Paciente: {pedido.paciente.id}', request)
        else:
            log_action(request.user, 'Pedido recusado', f'Vínculo recusado. Paciente: {pedido.paciente.id}', request)

        return Response({"success": True})
