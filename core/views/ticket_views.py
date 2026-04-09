from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.ticket import Ticket
from core.permissions import IsAdmin
from core.serializers.ticket_serializer import ResponderTicketSerializer, TicketSerializer
from core.services.log_action import log_action


class TicketListCreateView(APIView):
    """
    GET  /suporte/tickets/  — lista tickets do usuário autenticado (admin vê todos)
    POST /suporte/tickets/  — abre novo ticket (profissional ou responsavel)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.tipo_usuario == 'admin':
            qs = Ticket.objects.select_related('usuario', 'respondido_por').all()
            # filtro por status
            s = request.query_params.get('status')
            if s:
                qs = qs.filter(status=s)
        else:
            qs = Ticket.objects.filter(usuario=user)

        serializer = TicketSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.tipo_usuario == 'admin':
            raise PermissionDenied("Administradores não podem abrir tickets.")

        serializer = TicketSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ticket = serializer.save(usuario=user)
        log_action(
            user=user,
            acao='Abriu ticket de suporte',
            descricao=f'Ticket #{ticket.id}: {ticket.titulo}',
            request=request,
        )
        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class TicketDetailView(APIView):
    """
    GET   /suporte/tickets/<pk>/  — detalhe (dono ou admin)
    DELETE /suporte/tickets/<pk>/ — encerra ticket (dono ou admin)
    """
    permission_classes = [IsAuthenticated]

    def _get_ticket(self, pk, user):
        try:
            ticket = Ticket.objects.select_related('usuario', 'respondido_por').get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound("Ticket não encontrado.")
        if user.tipo_usuario != 'admin' and ticket.usuario != user:
            raise PermissionDenied("Você não tem acesso a este ticket.")
        return ticket

    def get(self, request, pk):
        ticket = self._get_ticket(pk, request.user)
        return Response(TicketSerializer(ticket).data)

    def delete(self, request, pk):
        ticket = self._get_ticket(pk, request.user)
        if ticket.status == 'fechado':
            return Response({"detail": "Ticket já está fechado."}, status=status.HTTP_400_BAD_REQUEST)
        ticket.status = 'fechado'
        ticket.save(update_fields=['status'])
        log_action(
            user=request.user,
            acao='Fechou ticket de suporte',
            descricao=f'Ticket #{ticket.id} encerrado.',
            request=request,
        )
        return Response(TicketSerializer(ticket).data)


class ResponderTicketView(APIView):
    """
    PATCH /suporte/tickets/<pk>/responder/  — admin responde ao ticket
    """
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound("Ticket não encontrado.")

        if ticket.status == 'fechado':
            return Response({"detail": "Não é possível responder um ticket fechado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ResponderTicketSerializer(ticket, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ticket = serializer.save(
            status='respondido',
            data_resposta=timezone.now(),
            respondido_por=request.user,
        )
        log_action(
            user=request.user,
            acao='Respondeu ticket de suporte',
            descricao=f'Ticket #{ticket.id} respondido.',
            request=request,
        )
        return Response(TicketSerializer(ticket).data)
