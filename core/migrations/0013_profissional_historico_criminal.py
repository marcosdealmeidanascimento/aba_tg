from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_admin_e_validacao_profissional'),
    ]

    operations = [
        migrations.AddField(
            model_name='profissional',
            name='historico_criminal',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='profissionais/documentos/',
                verbose_name='Histórico Criminal',
            ),
        ),
    ]
