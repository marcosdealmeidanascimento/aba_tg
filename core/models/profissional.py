from django.db import models


from backend import settings
from core.models.base import Genero
from .usuario import Usuario

class Profissional(models.Model):
    
    class Especialidade(models.TextChoices):
        PSICOLOGO = 'psicologo', 'Psicólogo'
        PSIQUIATRA = 'psiquiatra', 'Psiquiatra'
        FONOAUDIOLOGO = 'fonoaudiologo', 'Fonoaudiólogo'
        OUTRO = 'outro', 'Outro'

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profissional',
    )
    genero = models.CharField(
        choices=Genero.choices,
        max_length=20,
        null=True
    )
    licenca = models.CharField(max_length=50, unique=True, null=True)
    especialidade = models.CharField(
        max_length=20,
        choices=Especialidade.choices,
        default=Especialidade.PSICOLOGO
    )
    descricao = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"Profissional: {self.usuario.username}"