from django.contrib import admin
from oferente.models import Oferente, ubicacionesComercio
# Register your models here.

class OferenteAdmin(admin.ModelAdmin):
  list_display = ('nombrecomercio','usuario_creacion','fecha_creacion',
                  'usuario_modificacion','fecha_modificacion','eliminado','usuario_eliminacion','fecha_eliminacion')

admin.site.register(Oferente, OferenteAdmin)
admin.site.register(ubicacionesComercio)