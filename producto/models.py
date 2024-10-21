from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre=models.CharField(max_length=255)
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre=models.CharField(max_length=255)
    descripcion=models.TextField()
    imagen=models.ImageField(upload_to='productos/',null=True,blank=True)
    marca=models.CharField(verbose_name='Marca',max_length=255)
    categoria=models.ForeignKey(Subcategoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
#modelo para usar en supabase
class ProductoSupabase(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    marca=models.CharField(max_length=255)

    class Meta:
        # Apuntar este modelo a la base de datos de Supabase
        db_table = 'productos_supabase'
        managed = False  # No queremos que Django intente migrar esta tabla