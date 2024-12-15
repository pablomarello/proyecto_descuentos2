from django.forms import ValidationError
from django.utils import timezone
from crum import get_current_user
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.timezone import now

class Categoria(models.Model):
    nombre=models.CharField(max_length=255)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='categorias_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='categorias_modificadas')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    eliminado = models.BooleanField(default=False) #para la eliminacion logica
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='categorias_eliminadas')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.usuario_creacion = user
            else:
                self.usuario_modificacion = user
        super(Categoria, self).save()
    
    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

class Subcategoria(models.Model):
    nombre=models.CharField(max_length=255)
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='subcategorias_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='subcategorias_modificadas')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    eliminado = models.BooleanField(default=False) #para la eliminacion logica
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='subcategorias_eliminadas')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.usuario_creacion = user
            else:
                self.usuario_modificacion = user
        super(Subcategoria, self).save()
    
    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre=models.CharField(max_length=255)
    descripcion=models.TextField(max_length=300)
    imagen=models.ImageField(upload_to='productos/',null=True,blank=True)
    marca=models.CharField(verbose_name='Marca',max_length=255)
    categoria=models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         null=True, blank=True, related_name='productos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                             null=True, blank=True, related_name='productos_modificados')
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    eliminado = models.BooleanField(default=False) #para la eliminacion logica
    usuario_eliminacion = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                            null=True, blank=True, related_name='productos_eliminados')
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def save(self, force_insert = False, force_update = False, using = None,
              update_fields = None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.usuario_creacion = user
            else:
                self.usuario_modificacion = user
        super(Producto, self).save()

    def delete(self, using=None, keep_parents=False):
        user = get_current_user()
        if user is not None:
            self.usuario_eliminacion = user
        self.fecha_eliminacion = timezone.now()
        self.eliminado = True
        self.save()

    def clean(self):
        if Producto.objects.filter(nombre=self.nombre, eliminado=False).exists():
            raise ValidationError({'nombre': "Este producto ya existe."})

# funcion para enviar la señal luego del eliminado logico guarda el usuario y la fecha que elimino el producto 
def set_eliminacion_info(sender, instance, **kwargs):
    if instance.eliminado:  # Verifica si está siendo marcado como eliminado
        user = get_current_user()
        if user: 
            instance.usuario_eliminacion = user
        instance.fecha_eliminacion = now()
    

pre_save.connect(set_eliminacion_info, sender = Producto )
pre_save.connect(set_eliminacion_info, sender = Categoria )
pre_save.connect(set_eliminacion_info, sender = Subcategoria )
    
#modelo para usar en supabase
"""class ProductoSupabase(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    marca=models.CharField(max_length=255)

    class Meta:
        # Apuntar este modelo a la base de datos de Supabase
        db_table = 'productos_supabase'
        managed = False  # No queremos que Django intente migrar esta tabla"""