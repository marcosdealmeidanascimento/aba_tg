from django.db import models
from core.models.usuario import Usuario


class Profissional(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # --- UPLOADS (Novos campos) ---
    foto_perfil = models.ImageField(
        upload_to='profissionais/fotos/',
        null=True,
        blank=True,
        verbose_name="Foto de Perfil"
    )

    # --- DADOS BÁSICOS (Conforme a primeira seção do formulário) ---
    nome = models.CharField(max_length=100, verbose_name="Nome", blank=True)
    sobrenome = models.CharField(max_length=100, verbose_name="Sobrenome", blank=True)

    # Registro pode ser CRM, CRP, CREFITO, etc.
    registro_profissional = models.CharField(
        max_length=50,
        verbose_name="Registro Profissional (CRP/CRM/etc)",
        help_text="Ex: CRP 06/123456",
        blank=True
    )

    especialidade_principal = models.CharField(
        max_length=100,
        verbose_name="Especialidade Principal",
        help_text="Ex: Psicólogo, Terapeuta Ocupacional",
        blank=True
    )

    anos_experiencia_aba = models.PositiveIntegerField(
        verbose_name="Anos de Experiência em ABA",
        null=True,
        blank=True
    )

    # --- FORMAÇÃO E QUALIFICAÇÕES (Conforme a segunda seção) ---
    formacao_academica = models.TextField(
        verbose_name="Formação Acadêmica",
        help_text="Descreva sua graduação e pós-graduações...",
        blank=True
    )

    certificacoes = models.CharField(
        max_length=255,
        verbose_name="Certificações (BCBA, QBA, etc)",
        help_text="Liste suas certificações principais",
        blank=True
    )

    # Campo para upload do certificado/currículo em PDF
    arquivo_curriculo = models.FileField(
        upload_to='profissionais/documentos/',
        null=True,
        blank=True,
        verbose_name="Currículo/Certificados (PDF)"
    )

    bio_descricao = models.TextField(
        verbose_name="Bio / Descrição Profissional",
        help_text="Fale um pouco sobre sua atuação e abordagem...",
        blank=True
    )
    genero = models.CharField(
        max_length=25,
        verbose_name="Genero",
        help_text="Genero",
        blank=True
    )
    # --- ATENDIMENTO (Conforme a terceira seção) ---
    atendimento_logradouro = models.CharField(
        max_length=100,
        verbose_name="Logradouro",
        blank=True
    )
    atendimento_numero = models.CharField(
        max_length=10,
        verbose_name="N°",
        blank=True
    )
    atendimento_complemento = models.CharField(
        max_length=100,
        verbose_name="Complemento",
        blank=True
    )
    atendimento_bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro",
        blank=True
    )
    atendimento_cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade",
        blank=True
    )
    atendimento_cep = models.CharField(
        max_length=8,
        verbose_name="CEP",
        blank=True
    )
    atendimento_uf = models.CharField(
        max_length=2,
        verbose_name="UF",
        blank=True
    )

    # --- CONTATO (Conforme a quarta seção) ---
    telefone_contato = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        blank=True
    )

    email_contato = models.EmailField(
        verbose_name="E-mail de Contato",
        blank=True
    )

    # --- Documentos ---
    diploma = models.FileField(
        upload_to='profissionais/documentos/',
        null=True,
        blank=True,
        verbose_name="Diploma"
    )
    curriculo = models.FileField(
        upload_to='profissionais/documentos/',
        null=True,
        blank=True,
        verbose_name="Curriculum Vitae"
    )

    # --- METADADOS ---
    data_cadastro = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.especialidade_principal}"
