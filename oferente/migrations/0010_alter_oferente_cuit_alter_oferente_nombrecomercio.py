from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0009_alter_oferente_nombrecomercio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferente',
            name='cuit',
            field=models.BigIntegerField(max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='oferente',
            name='nombrecomercio',
            field=models.CharField(db_column='nombreComercio', max_length=30),
        ),
    ]
