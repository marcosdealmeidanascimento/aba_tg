from django.db import models
from .profissional import Profissional


class DisponibilidadeProfissional(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='disponibilidades')
    data_horario_inicio = models.DateTimeField()
    data_horario_fim = models.DateTimeField()
    recorrente = models.BooleanField(default=False)
    dia_semana = models.IntegerField(null=True, blank=True)  # 0=Seg … 6=Dom
    ativo = models.BooleanField(default=True)

    def __str__(self):
        if self.recorrente:
            dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            dia = dias[self.dia_semana] if self.dia_semana is not None else '?'
            return f"Disponibilidade recorrente {dia} — {self.profissional}"
        return f"Disponibilidade {self.data_horario_inicio.strftime('%d/%m/%Y %H:%M')} — {self.profissional}"

    def is_ocupado(self):
        return self.pedidos.filter(status__in=['pendente', 'aceito']).exists()
