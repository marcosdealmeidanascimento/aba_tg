from django.db import models
from .paciente import Paciente
from .profissional import Profissional
from .habilidade import Nivel


class Diagnostico(models.Model):
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE,
        related_name='diagnosticos'
    )
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='diagnosticos_emitidos'
    )
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        related_name='diagnosticos'
    )
    observacoes = models.TextField(blank=True, null=True)
    data_diagnostico = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.paciente.nome} para {self.nivel.nome}"
