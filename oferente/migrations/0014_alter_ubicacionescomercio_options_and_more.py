# Generated by Django 5.0.4 on 2024-10-29 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0013_alter_ubicacionescomercio_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ubicacionescomercio',
            options={'managed': True, 'verbose_name': 'ubicacion_comercio', 'verbose_name_plural': 'ubicaciones_comercio'},
        ),
        migrations.AlterModelTable(
            name='ubicacionescomercio',
            table='ubicacion_comercio',
        ),
    ]