# Generated by Django 5.0.6 on 2024-09-10 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0004_alter_oferente_id_usuario'),
        ('persona', '0013_alter_ubicaciones_departamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oferente',
            name='direccion',
        ),
        migrations.AddField(
            model_name='oferente',
            name='categoria',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='oferente',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='oferente',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='oferente',
            name='fecha_eliminacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='oferente',
            name='habilitado',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='oferente',
            name='usuario_creacion',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='oferente',
            name='usuario_eliminacion',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ubicacionesComercio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barrio', models.CharField(max_length=100)),
                ('calle', models.CharField(blank=True, max_length=50, null=True)),
                ('altura', models.CharField(blank=True, max_length=20, null=True)),
                ('latitud', models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True)),
                ('longitud', models.DecimalField(blank=True, decimal_places=6, max_digits=11, null=True)),
                ('comercio_id', models.OneToOneField(blank=True, db_column='identificacion', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ubicaion', to='oferente.oferente')),
                ('departamento', models.ForeignKey(db_column='cod_depto', on_delete=django.db.models.deletion.CASCADE, to='persona.tabladepartamento')),
                ('localidad', models.ForeignKey(db_column='cod_ase', on_delete=django.db.models.deletion.CASCADE, to='persona.tablalocalidad')),
                ('municipio', models.ForeignKey(db_column='cod_agl', on_delete=django.db.models.deletion.CASCADE, to='persona.tablamunicipio')),
                ('pais', models.ForeignKey(db_column='cod_pais', on_delete=django.db.models.deletion.CASCADE, to='persona.tablapais')),
                ('provincia', models.ForeignKey(db_column='cod_pcia', on_delete=django.db.models.deletion.CASCADE, to='persona.tablaprovincia')),
            ],
            options={
                'verbose_name': 'Ubicacion comercio',
                'verbose_name_plural': 'Ubicaciones comercio',
                'db_table': 'ubicacionComercio',
            },
        ),
    ]