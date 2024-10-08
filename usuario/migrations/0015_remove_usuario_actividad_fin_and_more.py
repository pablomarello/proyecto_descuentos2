# Generated by Django 5.0.4 on 2024-09-14 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_rol_permisos_alter_rol_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='actividad_fin',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='actividad_inicio',
        ),
        migrations.CreateModel(
            name='ActividadUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividadinicio', models.DateTimeField(blank=True, null=True)),
                ('actividadfin', models.DateTimeField(blank=True, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
