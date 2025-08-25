from django.db import models
from .usuario import Usuario

class Profissional(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    licenca = models.CharField(max_length=50, unique=True, null=True)
    especialidade = models.CharField(max_length=100)
    # Adicione outros campos de profissional aqui
    
    def __str__(self):
        return f"Profissional: {self.usuario.username}"