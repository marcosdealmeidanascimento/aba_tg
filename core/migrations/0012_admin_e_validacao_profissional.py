from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_disponibilidade_pedidoagendamento_sessao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(
                choices=[
                    ('profissional', 'Profissional'),
                    ('responsavel', 'Responsável'),
                    ('admin', 'Administrador'),
                ],
                default='responsavel',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='profissional',
            name='status_validacao',
            field=models.CharField(
                choices=[
                    ('pendente', 'Pendente'),
                    ('aprovado', 'Aprovado'),
                    ('rejeitado', 'Rejeitado'),
                ],
                default='pendente',
                max_length=20,
                verbose_name='Status de Validação',
            ),
        ),
        migrations.AddField(
            model_name='profissional',
            name='crp_validado',
            field=models.BooleanField(default=False, verbose_name='CRP/Registro Validado'),
        ),
        migrations.AddField(
            model_name='profissional',
            name='historico_criminal_aprovado',
            field=models.BooleanField(default=False, verbose_name='Histórico Criminal Aprovado'),
        ),
        migrations.AddField(
            model_name='profissional',
            name='notas_admin',
            field=models.TextField(blank=True, verbose_name='Notas do Administrador'),
        ),
    ]
