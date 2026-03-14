from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models.disponibilidade_profissional import DisponibilidadeProfissional
from core.serializers.disponibilidade_serializer import DisponibilidadeSerializer


def _expand_recorrente(slot, weeks=4):
    """Expands a recurring slot into concrete instances for the next `weeks` weeks."""
    today = timezone.now().date()
    instances = []
    for week_offset in range(weeks):
        # Find the next occurrence of dia_semana starting from today + week_offset*7
        base = today + timedelta(weeks=week_offset)
        # days ahead until the target weekday
        days_ahead = (slot.dia_semana - base.weekday()) % 7
        occurrence_date = base + timedelta(days=days_ahead)

        # Build a pseudo-instance dict (not saved to DB)
        duration = slot.data_horario_fim - slot.data_horario_inicio
        start = timezone.datetime.combine(occurrence_date, slot.data_horario_inicio.time(),
                                          tzinfo=slot.data_horario_inicio.tzinfo)
        end = start + duration

        if start < timezone.now():
            continue

        instances.append({
            'id': slot.id,
            'profissional': slot.profissional_id,
            'data_horario_inicio': start,
            'data_horario_fim': end,
            'recorrente': True,
            'dia_semana': slot.dia_semana,
            'ativo': slot.ativo,
            'ocupado': slot.is_ocupado(),
        })
    return instances


class DisponibilidadeProfissionalViewSet(viewsets.ModelViewSet):
    serializer_class = DisponibilidadeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        profissional_id = self.request.query_params.get('profissional')

        if profissional_id:
            # Responsável listing another professional's free slots
            return DisponibilidadeProfissional.objects.filter(
                profissional_id=profissional_id,
                ativo=True,
            )

        if hasattr(user, 'profissional'):
            return DisponibilidadeProfissional.objects.filter(
                profissional=user.profissional
            )

        return DisponibilidadeProfissional.objects.none()

    def list(self, request, *args, **kwargs):
        profissional_id = request.query_params.get('profissional')
        now = timezone.now()

        if profissional_id:
            # Return expanded slots (non-recurring future + recurring expanded)
            slots = self.get_queryset()
            result = []
            for slot in slots:
                if slot.recorrente:
                    result.extend(_expand_recorrente(slot, weeks=4))
                else:
                    if slot.data_horario_inicio > now and not slot.is_ocupado():
                        result.append(DisponibilidadeSerializer(slot).data)
            return Response(result)

        # Professional listing their own slots (future, active)
        qs = self.get_queryset().filter(data_horario_inicio__gt=now)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem cadastrar disponibilidades.")
        serializer.save(profissional=user.profissional)

    def perform_update(self, serializer):
        user = self.request.user
        if not hasattr(user, 'profissional'):
            raise PermissionDenied("Apenas profissionais podem editar disponibilidades.")
        if serializer.instance.profissional != user.profissional:
            raise PermissionDenied("Você não é o dono deste slot.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not hasattr(user, 'profissional') or instance.profissional != user.profissional:
            raise PermissionDenied("Você não é o dono deste slot.")
        instance.delete()
