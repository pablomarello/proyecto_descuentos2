from django.db import models
from persona.models import TablaDepartamento, TablaLocalidad, TablaMunicipio, TablaPais, TablaProvincia
from usuario.models import Usuario, Rol

class Oferente(models.Model):

    nombrecomercio = models.CharField(db_column='nombreComercio', max_length=30)  # Field name made lowercase.
    cuit=models.BigIntegerField(null=False,unique=True,max_length=11)
    categoria=models.CharField(max_length=25, null=True, blank=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comercios', db_column='id_usuario',null=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.nombrecomercio

    class Meta:
        managed = True
        db_table = 'oferente'



class ubicacionesComercio(models.Model):
    comercio_id=models.OneToOneField(Oferente,blank=True,null=True,on_delete=models.CASCADE,db_column="oferente_id")
    pais=models.ForeignKey(TablaPais,blank=False,null=True,on_delete=models.CASCADE,db_column="cod_pais")
    provincia=models.ForeignKey(TablaProvincia,blank=False,null=True,on_delete=models.CASCADE,db_column="cod_pcia")
    departamento=models.ForeignKey(TablaDepartamento,blank=False,null=True,on_delete=models.CASCADE,db_column="cod_depto")
    municipio=models.ForeignKey(TablaMunicipio,blank=False,null=True,on_delete=models.CASCADE,db_column="cod_agl")
    localidad=models.ForeignKey(TablaLocalidad,blank=False,null=True,on_delete=models.CASCADE,db_column="cod_ase")
    barrio=models.CharField(max_length=100,blank=False,null=False)
    calle=models.CharField(max_length=50,blank=True,null=True)
    altura=models.CharField(max_length=20,blank=True,null=True)
    latitud = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    #lat
    #long
    class Meta:
        verbose_name='ubicacion_comercio'
        db_table= 'ubicacion_comercio'
        managed=True