from django.db import models
from .atividade import Atividade
from .sessao import Sessao
from .profissional import Profissional
from .paciente import Paciente


class ExecucaoAtividade(models.Model):
    STATUS_CHOICES = [
        ('sem_auxilio', 'Correta'),
        ('ajuda', 'Precisou Ajuda'),
        ('dificuldade', 'Teve Dificuldade'),
        ('nao_realizou', 'Não Realizou'),
        ('outro', 'Outro')
    ]
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='execucoes')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.SET_NULL, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
