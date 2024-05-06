from django.db import models
from django.conf import settings

class Personas(models.Model):

    
    identificacion= models.CharField(max_length=10, primary_key=True,help_text='Ingrese el nro de dni sin puntos')
    nombres=models.CharField(max_length=50, help_text='Si posee mas de un nombre ingrese los mismos con un espacio entre cada nombre. Ej: Juan Carlos',null=True,blank=True)
    apellidos=models.CharField(max_length=25, help_text='Si posee mas de un apellido ingrese los mismos con un espacio entre cada apellido. Ej: Rodriguez Perez',null=True,blank=True)
    genero=models.CharField(max_length=15,null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    foto=models.ImageField(upload_to='personas/',default='avatar_default.png',null=True,blank=True)
    usuario_creacion= models.PositiveIntegerField(null=True,blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)
    
    

    class Meta:
        verbose_name='Personas'
        verbose_name_plural= 'Personas'
        db_table= 'personas'
# Create your models here.