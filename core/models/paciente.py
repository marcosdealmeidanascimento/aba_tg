from django.db import models
from core.models.base import Genero
from core.models.profissional import Profissional
from core.models.responsavel import Responsavel


class Paciente(models.Model):
    nome = models.CharField(max_length=2020)
    data_nascimento = models.DateField()
    genero = models.CharField(
        max_length=10,
        choices=Genero.choices,
        default=Genero.OUTRO
    )
    descricao = models.TextField(null=True)

    responsaveis = models.ManyToManyField(
        Responsavel,
        related_name='pacientes_cuidados',
    )

    profissionais = models.ManyToManyField(
        Profissional,
        related_name='pacientes_atendidos',
        blank=True
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"Paciente: {self.nome}")
