# Generated by Django 5.0.4 on 2024-09-05 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0012_alter_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario'),
        ),
    ]