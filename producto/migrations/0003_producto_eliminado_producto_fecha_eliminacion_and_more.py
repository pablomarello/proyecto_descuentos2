# Generated by Django 5.0.4 on 2024-12-11 03:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_producto_fecha_creacion_producto_fecha_modificacion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producto',
            name='fecha_eliminacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='usuario_eliminacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos_eliminados', to=settings.AUTH_USER_MODEL),
        ),
    ]