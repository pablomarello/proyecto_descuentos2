from django.contrib import admin

from oferta.models import Oferta,Comentario

class OfertaAdmin(admin.ModelAdmin):
  list_display = ('titulo','descripcion', 'get_productos','oferente','usuario_creacion','fecha_creacion',
                  'usuario_modificacion','fecha_modificacion','eliminado','usuario_eliminacion','fecha_eliminacion')
  
  def get_productos(self, obj):
        return ", ".join([producto.nombre for producto in obj.productos.all()])
  
  get_productos.short_description = 'Producto'

admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Comentario)
# Register your models here.
