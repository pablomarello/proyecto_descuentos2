# Generated by Django 5.0.4 on 2024-10-09 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0006_remove_oferente_usuario_creacion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferente',
            name='cuit',
            field=models.BigIntegerField(max_length=11, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='oferente',
            name='id_usuario',
            field=models.ForeignKey(db_column='id_usuario', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comercios', to=settings.AUTH_USER_MODEL),
        ),
    ]
