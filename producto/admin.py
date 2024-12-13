from django.contrib import admin
from producto.models import Producto, Categoria,Subcategoria

# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
  list_display = ('nombre','descripcion','imagen','marca','categoria','usuario_creacion','fecha_creacion',
                  'usuario_modificacion','fecha_modificacion','eliminado','usuario_eliminacion','fecha_eliminacion')
  
class CategoriaAdmin(admin.ModelAdmin):
  list_display = ('nombre','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion',
                  'eliminado','usuario_eliminacion','fecha_eliminacion')
  
class SubcategoriaAdmin(admin.ModelAdmin):
  list_display = ('nombre','usuario_creacion','fecha_creacion','usuario_modificacion','fecha_modificacion',
                  'eliminado','usuario_eliminacion','fecha_eliminacion')
 

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Subcategoria)
