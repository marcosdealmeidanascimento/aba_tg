from django.db import models
from django.utils import timezone
from .paciente import Paciente
from .profissional import Profissional


class Sessao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='sessoes')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='sessoes_criadas')
    data_horario_inicio = models.DateTimeField(default=timezone.now)
    data_horario_fim = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sessão de {self.paciente} - {self.data_horario_inicio.strftime('%d/%m/%Y %H:%M')}"
