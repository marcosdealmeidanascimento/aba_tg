from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework import viewsets

from core.models import Paciente
from core.permissions import IsRelatedToPaciente
from core.serializers.paciente_serializers import PacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsRelatedToPaciente()]

    def get_queryset(self):
        """
        Filtra a lista de pacientes com base no usuário logado.
        """
        user = self.request.user
        if user.tipo_usuario == 'profissional':
            return user.profissional.pacientes_atendidos.all()

        if user.tipo_usuario == 'responsavel':
            return user.responsavel.pacientes_cuidados.all()

        return Paciente.objects.none()

    def perform_create(self, serializer):
        """
        Verifica se o usuário é um responsável antes de criar o paciente e
        associa o paciente a ele.
        """
        user = self.request.user
        if not hasattr(user, 'responsavel'):
            raise PermissionDenied("Apenas responsáveis podem criar pacientes.")

        serializer.context['responsavel_logado'] = user.responsavel
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        # Lógica para adicionar ou remover profissionais
        profissionais_data = self.request.data.get('profissionais', None)
        if profissionais_data is not None:
            serializer.instance.profissionais.set(profissionais_data)

        # Lógica para adicionar ou remover responsáveis
        responsaveis_data = self.request.data.get('responsaveis', None)
        if responsaveis_data is not None and user.id in responsaveis_data:
            serializer.instance.responsaveis.set(responsaveis_data)

        serializer.save()

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except Paciente.DoesNotExist:
            raise NotFound("Paciente não encontrado.")
