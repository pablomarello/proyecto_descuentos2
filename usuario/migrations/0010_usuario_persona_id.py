# Generated by Django 5.0.4 on 2024-05-10 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_remove_persona_usuario_id'),
        ('usuario', '0009_remove_usuario_persona_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='persona_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='persona.persona'),
        ),
    ]