# Generated by Django 5.0.6 on 2024-09-10 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0012_alter_ubicaciones_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ubicaciones',
            name='departamento',
            field=models.ForeignKey(db_column='cod_depto', on_delete=django.db.models.deletion.CASCADE, to='persona.tabladepartamento'),
        ),
    ]
