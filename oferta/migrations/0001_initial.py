# Generated by Django 5.0.4 on 2024-10-12 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oferente', '0009_alter_oferente_nombrecomercio'),
        ('producto', '0002_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(blank=True, max_length=50)),
                ('descripcion', models.TextField(blank=True, max_length=150)),
                ('precio_normal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_oferta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('activo', models.BooleanField(default=True)),
                ('oferente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='oferente.oferente')),
                ('productos', models.ManyToManyField(related_name='ofertas', to='producto.producto')),
            ],
        ),
    ]
