# Generated by Django 5.0.6 on 2024-05-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0004_alter_persona_identificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='identificacion',
            field=models.IntegerField(help_text='Ingrese el nro de dni sin puntos', primary_key=True, serialize=False, verbose_name='D.N.I.'),
        ),
    ]