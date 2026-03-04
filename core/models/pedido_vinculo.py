from django.db import models
from core.models.profissional import Profissional
from core.models.responsavel import Responsavel
from core.models.paciente import Paciente


class PedidoVinculo(models.Model):
    STATUS_CHOICES = [('pendente', 'Pendente'), ('aceito', 'Aceito'), ('recusado', 'Recusado')]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)
