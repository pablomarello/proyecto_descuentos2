# Generated by Django 5.0.4 on 2024-10-30 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0014_alter_ubicacionescomercio_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ubicacionescomercio',
            name='comercio_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oferente.oferente'),
        ),
    ]
