from django.db import models
from django.conf import settings
#from usuario.models import Usuario

class Persona(models.Model):
    GENERO=[('M','Masculino'),
                ('F','Femenino'),
                ('N','No Binario')]
    
    identificacion= models.IntegerField( primary_key=True, verbose_name='D.N.I.', help_text='Ingrese el nro de dni sin puntos')
    nombres=models.CharField(max_length=50, help_text='Si posee mas de un nombre ingrese los mismos con un espacio entre cada nombre. Ej: Juan Carlos',null=True,blank=True)
    apellidos=models.CharField(max_length=25, help_text='Si posee mas de un apellido ingrese los mismos con un espacio entre cada apellido. Ej: Rodriguez Perez',null=True,blank=True)
    genero=models.CharField(max_length=15,choices=GENERO,null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    foto=models.ImageField(upload_to='personas/',default='avatar_default.png',null=True,blank=True)
    usuario_creacion= models.PositiveIntegerField(null=True,blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)

    #usuario_id = models.OneToOneField(Usuario, on_delete=models.CASCADE, blank=True,null=True)
    
    

    class Meta:
        verbose_name='Persona'
        verbose_name_plural= 'Personas'
        db_table= 'persona'
# Create your models here.