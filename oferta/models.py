from datetime import timezone
from django.db import models

from oferente.models import Oferente
from producto.models import Producto
from usuario.models import Usuario

class Oferta(models.Model):
    titulo = models.TextField(max_length=50, blank=True)
    descripcion = models.TextField(max_length=150, blank=True)
    precio_normal = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto, related_name='ofertas')
    oferente = models.ForeignKey(Oferente, on_delete=models.CASCADE, related_name='ofertas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)    
    eliminado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='ofertas/',default='default_image.png',null=True,blank=True)
    
    class Meta:
        Managed:True
    
    def __str__(self):
        return self.titulo
    
# Create your models here.


class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    fecha_votacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oferta')  # Evita que un usuario vote más de una vez por la misma oferta


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=100,null=True)
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oferta')  # Evita que un usuario comente más de una vez por la misma oferta
