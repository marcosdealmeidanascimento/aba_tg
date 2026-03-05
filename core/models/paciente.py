from django.db import models
from core.models.profissional import Profissional
from core.models.responsavel import Responsavel


class Paciente(models.Model):
    foto_paciente = models.ImageField(
        upload_to='pacientes/fotos/',
        null=True,
        blank=True,
        verbose_name="Foto do Paciente"
    )
    nome = models.CharField(max_length=255, blank=True)
    data_nascimento = models.DateField()
    genero = models.CharField(
        max_length=25,
        verbose_name="Genero",
        help_text="Genero",
        blank=True,
        null=True,
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"Paciente: {self.nome}")
