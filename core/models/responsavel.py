from django.db import models
from .usuario import Usuario
from core.models.base import Genero


class Responsavel(models.Model):
    class Parentesco(models.IntegerChoices):
        PAI = 1, "Pai"
        MAE = 2, "Mãe"
        TIO = 5, "Tio(a)"
        IRMAO = 6, "Irmão(ã)"
        OUTRO = 7, "Outro"

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    genero = models.CharField(
        choices=Genero.choices,
        null=True
    )
    parentesco = models.PositiveSmallIntegerField(
        "Parentesco",
        choices=Parentesco.choices,
        default=Parentesco.OUTRO
    )

    def __str__(self):
        return f"Responsável: {self.usuario.username}"
