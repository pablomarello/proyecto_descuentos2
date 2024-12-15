from django.utils import timezone
from crum import get_current_user
from django.db import models
from persona.models import TablaDepartamento, TablaLocalidad, TablaMunicipio, TablaPais, TablaProvincia
from usuario.models import Usuario, Rol
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.timezone import now

class Oferente(models.Model):

    nombrecomercio = models.CharField(db_column='nombreComercio', max_length=30)  # Field name made lowercase.
    cuit=models.BigIntegerField(null=False,unique=True,max_length=11)
    categoria=models.CharField(max_length=25, null=True, blank=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comercios', db_column='id_usuario',null=True)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='oferentes_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='oferentes_modificados')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='oferentes_eliminados')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)


    
    def __str__(self):
        return self.nombrecomercio
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.usuario_creacion = user
            else:
                self.usuario_modificacion = user
        super(Oferente, self).save()

    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

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

# funcion para enviar la señal luego del eliminado logico guarda el usuario y la fecha que elimino al comercio(oferente) 
def set_eliminacion_info(sender, instance, **kwargs):
    if instance.eliminado:  # Verifica si está siendo marcado como eliminado
        user = get_current_user()
        if user: 
            instance.usuario_eliminacion = user
        instance.fecha_eliminacion = now()
    

pre_save.connect(set_eliminacion_info, sender = Oferente )