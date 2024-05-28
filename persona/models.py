from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
# from django.utils.crypto import get_random_string
import os
from PIL import Image
#from usuario.models import Usuario

""" pone el nro de dni como nombre de la foto/imagen cargada """
def get_file_path(instance, filename):
    ext = 'png'  # Establecemos la extensión a png
    filename = f"fotopersona_{instance.identificacion}.{ext}"
    return os.path.join('personas/', filename)

class Persona(models.Model):
    GENERO=[('M','Masculino'),
                ('F','Femenino'),
                ('N','No Binario')]
    
    identificacion= models.IntegerField( primary_key=True, verbose_name='D.N.I.', help_text='Ingrese el nro de dni sin puntos')
    nombres=models.CharField(max_length=50, help_text='Si posee mas de un nombre ingrese los mismos con un espacio entre cada nombre. Ej: Juan Carlos',null=True,blank=True)
    apellidos=models.CharField(max_length=25, help_text='Si posee mas de un apellido ingrese los mismos con un espacio entre cada apellido. Ej: Rodriguez Perez',null=True,blank=True)
    genero=models.CharField(max_length=15,choices=GENERO,null=True,blank=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    foto=models.ImageField(upload_to=get_file_path,default='avatar_default.png',null=True,blank=True)
    usuario_creacion= models.PositiveIntegerField(null=True,blank=True)
    habilitado = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion= models.DateTimeField(null=True,blank=True)
    usuario_eliminacion= models.PositiveIntegerField(null=True,blank=True)
    #usuario_id = models.OneToOneField(Usuario, on_delete=models.CASCADE, blank=True,null=True)
    
    def save(self, *args, **kwargs):
        # Primero se guarda la instancia para asegurarse de que tiene un ID
        super().save(*args, **kwargs)
        # Convertir la imagen a PNG
        if self.foto and not self.foto.name.endswith('.png'):
            img = Image.open(self.foto)
            png_io = BytesIO()
            img.save(png_io, format='PNG')
            self.foto.save(self.foto.name, ContentFile(png_io.getvalue()), save=False)
        # Luego se guarda de nuevo para actualizar el nombre del archivo si es necesario
        self.foto.name = get_file_path(self, self.foto.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name='Persona'
        verbose_name_plural= 'Personas'
        db_table= 'persona'
# Create your models here.