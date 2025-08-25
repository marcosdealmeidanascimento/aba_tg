# core/models/usuario.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    USER_TYPE_CHOICES = (
        ("profissional", "Profissional"),
        ("responsavel", "Responsável"),
    )
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default="responsavel"
    )

    # Adicione estas duas linhas para resolver o conflito de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )