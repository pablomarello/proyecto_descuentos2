# Generated by Django 5.0.4 on 2024-05-10 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_persona_usuario_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='usuario_id',
        ),
    ]
