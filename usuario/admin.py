from django.contrib import admin
from usuario.models import Usuario, Rol, ActividadUsuario

# Register your models here.


admin.site.register(Usuario)
admin.site.register(Rol)
# Register your models here.


class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'actividadinicio', 'actividadfin')
    list_filter = ('usuario', 'actividadinicio', 'actividadfin')
    search_fields = ('usuario__username',)
    readonly_fields = ('actividadinicio', 'actividadfin')

admin.site.register(ActividadUsuario, ActividadUsuarioAdmin)