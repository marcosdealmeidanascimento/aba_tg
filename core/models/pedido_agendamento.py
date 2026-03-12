from django.db import models
from .paciente import Paciente
from .profissional import Profissional
from .responsavel import Responsavel
from .habilidade import Nivel


class PedidoAgendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='pedidos_agendamento')
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE, related_name='pedidos_agendamento_criados')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='pedidos_agendamento_recebidos')
    nivel = models.ForeignKey(Nivel, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_agendamento')
    data_horario_proposta = models.DateTimeField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    motivo_recusa = models.TextField(blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    sessao_criada = models.OneToOneField(
        'Sessao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedido_agendamento',
    )

    def __str__(self):
        return f"Agendamento {self.status} — {self.paciente} em {self.data_horario_proposta.strftime('%d/%m/%Y %H:%M')}"
