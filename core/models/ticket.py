from django.db import models
from core.models.usuario import Usuario


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('aberto', 'Aberto'),
        ('respondido', 'Respondido'),
        ('fechado', 'Fechado'),
    )

    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensagem = models.TextField(verbose_name="Mensagem")
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Usuário"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto',
        verbose_name="Status"
    )
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data de abertura")
    resposta = models.TextField(blank=True, verbose_name="Resposta do admin")
    data_resposta = models.DateTimeField(null=True, blank=True, verbose_name="Data da resposta")
    respondido_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_respondidos',
        verbose_name="Respondido por"
    )

    class Meta:
        verbose_name = "Ticket de Suporte"
        verbose_name_plural = "Tickets de Suporte"
        ordering = ['-data']

    def __str__(self):
        return f"#{self.id} — {self.titulo} ({self.status})"
