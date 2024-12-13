from crum import get_current_user
from django.utils import timezone
#from datetime import timezone
from django.db import models
from django.conf import settings
from oferente.models import Oferente
from producto.models import Producto
from usuario.models import Usuario
from django.db.models.signals import pre_save
from django.utils.timezone import now

class Oferta(models.Model):
    titulo = models.TextField(max_length=50)
    descripcion = models.TextField(max_length=150)
    precio_normal = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto, related_name='ofertas')
    oferente = models.ForeignKey(Oferente, on_delete=models.CASCADE, related_name='ofertas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)    
    eliminado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='ofertas/',default='default_image.png',null=True,blank=True)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='ofertas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='ofertas_modificadas')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='ofertas_eliminadas')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        Managed:True
    
    def __str__(self):
        return self.titulo
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.usuario_creacion = user
            else:
                self.usuario_modificacion = user
        super(Oferta, self).save()

    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

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

# funcion para enviar la señal luego del eliminado logico guarda el usuario y la fecha que elimino la oferta 
def set_eliminacion_info(sender, instance, **kwargs):
    if instance.eliminado:  # Verifica si está siendo marcado como eliminado
        user = get_current_user()
        if user: 
            instance.usuario_eliminacion = user
        instance.fecha_eliminacion = now()
    

pre_save.connect(set_eliminacion_info, sender = Oferta )
