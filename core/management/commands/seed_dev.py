from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Paciente, Profissional, Responsavel, Usuario


SENHA_ADMIN = "admin123"
SENHA_PROF = "prof123"
SENHA_RESP = "resp123"


class Command(BaseCommand):
    help = 'Limpa usuários e pacientes e cria dados de desenvolvimento (admin, profissional, responsavel, paciente)'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self._limpar()
            admin = self._criar_admin()
            prof = self._criar_profissional()
            resp = self._criar_responsavel()
            paciente = self._criar_paciente(prof, resp)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== Seed concluído ==="))
        self.stdout.write("")
        self.stdout.write(f"  Admin        | usuario: admin         | senha: {SENHA_ADMIN}")
        self.stdout.write(f"  Profissional | usuario: joao.silva    | senha: {SENHA_PROF}")
        self.stdout.write(f"  Responsavel  | usuario: carlos.souza  | senha: {SENHA_RESP}")
        self.stdout.write(f"  Paciente     | {paciente.nome} (id={paciente.pk})")
        self.stdout.write("")

    def _limpar(self):
        Paciente.objects.all().delete()
        Usuario.objects.all().delete()
        self.stdout.write("  Banco limpo (usuarios e pacientes removidos)")

    def _criar_admin(self):
        usuario = Usuario.objects.create(
            username="admin",
            email="admin@aba.com",
            first_name="Admin",
            last_name="Sistema",
            tipo_usuario="admin",
            is_staff=True,
            is_superuser=True,
        )
        usuario.set_password(SENHA_ADMIN)
        usuario.save()
        self.stdout.write(self.style.SUCCESS("  [CRIADO] Admin: admin@aba.com"))
        return usuario

    def _criar_profissional(self):
        usuario = Usuario.objects.create(
            username="joao.silva",
            email="joao.silva@clinica.com",
            first_name="João",
            last_name="Silva",
            tipo_usuario="profissional",
        )
        usuario.set_password(SENHA_PROF)
        usuario.save()

        profissional = Profissional.objects.create(
            usuario=usuario,
            nome="João",
            sobrenome="Silva",
            registro_profissional="CRP 06/123456",
            especialidade_principal="Psicólogo",
            anos_experiencia_aba=5,
            formacao_academica="Psicologia - USP (2015). Pós em ABA - PUC-SP (2018).",
            certificacoes="BCBA, QBA",
            bio_descricao="Especialista em ABA para crianças com TEA. Atendimento domiciliar e em clínica.",
            genero="Masculino",
            telefone_contato="11999990001",
            email_contato="joao.silva@clinica.com",
            atendimento_logradouro="Av. Paulista",
            atendimento_numero="1000",
            atendimento_complemento="Sala 42",
            atendimento_bairro="Bela Vista",
            atendimento_cidade="São Paulo",
            atendimento_cep="01310100",
            atendimento_uf="SP",
            status_validacao="aprovado",
            crp_validado=True,
            historico_criminal_aprovado=True,
        )
        self.stdout.write(self.style.SUCCESS("  [CRIADO] Profissional: joao.silva@clinica.com"))
        return profissional

    def _criar_responsavel(self):
        usuario = Usuario.objects.create(
            username="carlos.souza",
            email="carlos.souza@email.com",
            first_name="Carlos",
            last_name="Souza",
            tipo_usuario="responsavel",
        )
        usuario.set_password(SENHA_RESP)
        usuario.save()

        responsavel = Responsavel.objects.create(
            usuario=usuario,
            nome="Carlos",
            sobrenome="Souza",
            genero="Masculino",
            parentesco=Responsavel.Parentesco.PAI,
            telefone="11988880001",
            cpf="123.456.789-00",
            endereco="Rua das Flores, 42, Bela Vista, São Paulo/SP",
        )
        self.stdout.write(self.style.SUCCESS("  [CRIADO] Responsavel: carlos.souza@email.com"))
        return responsavel

    def _criar_paciente(self, prof, resp):
        paciente = Paciente.objects.create(
            nome="Lucas Souza",
            data_nascimento=date(2018, 3, 15),
            genero="Masculino",
            descricao="Diagnóstico de TEA nível 2. Iniciando protocolo de comunicação funcional.",
        )
        paciente.responsaveis.add(resp)
        paciente.profissionais.add(prof)
        self.stdout.write(self.style.SUCCESS(f"  [CRIADO] Paciente: Lucas Souza (id={paciente.pk})"))
        return paciente
