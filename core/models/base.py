from django.db import models


class Genero(models.TextChoices):
    MASCULINO = 'masculino', 'Masculino'
    FEMININO = 'feminino', 'Feminino'
    OUTRO = 'outro', 'Outro'