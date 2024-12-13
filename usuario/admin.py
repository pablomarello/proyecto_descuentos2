from django.contrib import admin
from usuario.models import Usuario, Rol, ActividadUsuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username','email','persona_id','usuario_creacion','fecha_creacion',
                  'usuario_modificacion','fecha_modificacion','eliminado','usuario_eliminacion','fecha_eliminacion')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
# Register your models here.


class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'actividadinicio', 'actividadfin')
    list_filter = ('usuario', 'actividadinicio', 'actividadfin')
    search_fields = ('usuario__username',)
    readonly_fields = ('actividadinicio', 'actividadfin')

admin.site.register(ActividadUsuario, ActividadUsuarioAdmin)