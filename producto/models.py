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