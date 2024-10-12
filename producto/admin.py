from django.contrib import admin
from producto.models import Producto, Categoria,Subcategoria

# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
