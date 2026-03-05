from django.db import models
from .usuario import Usuario


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
        primary_key=True,
        related_name='responsavel'
    )

    # --- NOVO: Foto e Dados de Identificação ---
    foto_perfil = models.ImageField(
        upload_to='responsaveis/fotos/',
        null=True,
        blank=True,
        verbose_name="Foto de Perfil"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome", blank=True,)
    sobrenome = models.CharField(max_length=100, verbose_name="Sobrenome", blank=True,)

    genero = models.CharField(
        max_length=25,
        verbose_name="Genero",
        help_text="Genero",
        blank=True,
        null=True,
    )
    parentesco = models.PositiveSmallIntegerField(
        "Parentesco",
        choices=Parentesco.choices,
        default=Parentesco.OUTRO,
        blank=True,
    )

    # --- NOVO: Campos da Imagem ---
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name="CPF")
    endereco = models.TextField(verbose_name="Endereço Completo", null=True, blank=True)

    def __str__(self):
        return f"Responsável: {self.nome} {self.sobrenome} ({self.usuario.username})"
