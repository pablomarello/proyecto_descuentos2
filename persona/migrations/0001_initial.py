# Generated by Django 5.0.4 on 2024-05-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('identificacion', models.CharField(help_text='Ingrese el nro de dni sin puntos', max_length=10, primary_key=True, serialize=False, verbose_name='D.N.I.')),
                ('nombres', models.CharField(blank=True, help_text='Si posee mas de un nombre ingrese los mismos con un espacio entre cada nombre. Ej: Juan Carlos', max_length=50, null=True)),
                ('apellidos', models.CharField(blank=True, help_text='Si posee mas de un apellido ingrese los mismos con un espacio entre cada apellido. Ej: Rodriguez Perez', max_length=25, null=True)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('N', 'No Binario')], max_length=15, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('foto', models.ImageField(blank=True, default='avatar_default.png', null=True, upload_to='personas/')),
                ('usuario_creacion', models.PositiveIntegerField(blank=True, null=True)),
                ('habilitado', models.BooleanField(default=True)),
                ('eliminado', models.BooleanField(default=False)),
                ('fecha_eliminacion', models.DateTimeField(blank=True, null=True)),
                ('usuario_eliminacion', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'db_table': 'persona',
            },
        ),
    ]
