from django.db import models


class Modulo(models.Model):
    nome = models.CharField(max_length=5, unique=True)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.descricao}"


class Nivel(models.Model):
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='niveis'
    )
    nome = models.CharField(max_length=5)
    descricao = models.TextField()

    class Meta:
        unique_together = ('modulo', 'nome')

    def __str__(self):
        return f"{self.modulo.nome} - {self.nome} - {self.descricao}"
