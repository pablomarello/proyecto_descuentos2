# Generated by Django 5.0.4 on 2024-09-18 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0005_remove_oferente_direccion_oferente_categoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oferente',
            name='usuario_creacion',
        ),
    ]
