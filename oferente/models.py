from django.db import models
from usuario.models import Usuario

class Oferente(models.Model):
    nombrecomercio = models.CharField(db_column='nombreComercio', max_length=30)  # Field name made lowercase.
    direccion = models.CharField(max_length=50)
    cuit=models.BigIntegerField(null=False,unique=True,max_length=11)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario',null=True)

    class Meta:
        managed = True
        db_table = 'oferente'
