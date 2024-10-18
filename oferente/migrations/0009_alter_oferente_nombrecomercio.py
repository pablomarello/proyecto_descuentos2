

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oferente', '0008_alter_oferente_id_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferente',
            name='nombrecomercio',
            field=models.CharField(db_column='nombreComercio'),
        ),
    ]
