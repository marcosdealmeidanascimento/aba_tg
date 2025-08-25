from django.db import models
from .usuario import Usuario

class Responsavel(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True
    )
    nome_da_crianca = models.CharField(max_length=100)
    parentesco = models.CharField(max_length=50)
    # Adicione outros campos de responsável aqui
    
    def __str__(self):
        return f"Responsável: {self.usuario.username}"