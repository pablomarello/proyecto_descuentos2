from django.db import models

from oferente.models import Oferente
from producto.models import Producto

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

    def __str__(self):
        return self.titulo
# Create your models here.
