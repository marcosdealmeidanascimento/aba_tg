import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_pedidoagendamento'),
    ]

    operations = [
        # 1. Create DisponibilidadeProfissional
        migrations.CreateModel(
            name='DisponibilidadeProfissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_horario_inicio', models.DateTimeField()),
                ('data_horario_fim', models.DateTimeField()),
                ('recorrente', models.BooleanField(default=False)),
                ('dia_semana', models.IntegerField(blank=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('profissional', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='disponibilidades',
                    to='core.profissional',
                )),
            ],
        ),

        # 2. Add disponibilidade FK to PedidoAgendamento
        migrations.AddField(
            model_name='pedidoagendamento',
            name='disponibilidade',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='pedidos',
                to='core.disponibilidadeprofissional',
            ),
        ),

        # 3. Add data_horario_fim_proposta to PedidoAgendamento
        migrations.AddField(
            model_name='pedidoagendamento',
            name='data_horario_fim_proposta',
            field=models.DateTimeField(blank=True, null=True),
        ),

        # 4. Add data_horario_fim_prevista to Sessao
        migrations.AddField(
            model_name='sessao',
            name='data_horario_fim_prevista',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
