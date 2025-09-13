from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.base import Genero
from .usuario import Usuario


class Profissional(models.Model):
    class Especialidade(models.TextChoices):
        PSICOLOGO = 'psicologo', _('Psicólogo')
        PSIQUIATRA = 'psiquiatra', _('Psiquiatra')
        FONOAUDIOLOGO = 'fonoaudiologo', _('Fonoaudiólogo')
        OUTRO = 'outro', _('Outro')

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    genero = models.CharField(
        max_length=10,
        choices=Genero.choices,
        default=Genero.OUTRO
    )
    licenca = models.CharField(max_length=50, unique=True)
    especialidade = models.CharField(
        max_length=20,
        choices=Especialidade.choices,
        default=Especialidade.OUTRO
    )
    descricao = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True)
    aprovado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(f"Profissional: {self.usuario.username}")
