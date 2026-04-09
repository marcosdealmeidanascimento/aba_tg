import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_profissional_historico_criminal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200, verbose_name='Título')),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
                ('status', models.CharField(
                    choices=[('aberto', 'Aberto'), ('respondido', 'Respondido'), ('fechado', 'Fechado')],
                    default='aberto',
                    max_length=20,
                    verbose_name='Status',
                )),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de abertura')),
                ('resposta', models.TextField(blank=True, verbose_name='Resposta do admin')),
                ('data_resposta', models.DateTimeField(blank=True, null=True, verbose_name='Data da resposta')),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tickets',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Usuário',
                )),
                ('respondido_por', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='tickets_respondidos',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Respondido por',
                )),
            ],
            options={
                'verbose_name': 'Ticket de Suporte',
                'verbose_name_plural': 'Tickets de Suporte',
                'ordering': ['-data'],
            },
        ),
    ]
