from django.db import models
from django.utils import timezone
from .paciente import Paciente
from .profissional import Profissional
from .responsavel import Responsavel
from .habilidade import Nivel


class Sessao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='sessoes')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=True, blank=True, related_name='sessoes_criadas')
    responsavel = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessoes_criadas')
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT, related_name='sessoes', null=True, blank=True)
    data_horario_inicio = models.DateTimeField(default=timezone.now)
    data_horario_fim = models.DateTimeField(null=True, blank=True)
    data_horario_fim_prevista = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sessão de {self.paciente} - {self.data_horario_inicio.strftime('%d/%m/%Y %H:%M')}"
