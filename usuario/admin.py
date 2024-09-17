from django.contrib import admin
from usuario.models import Usuario, Rol, ActividadUsuario

# Register your models here.

admin.site.register(Usuario)
@admin.register(Rol)
class RolaAdmin(admin.ModelAdmin):
    list_display = ('rol',)
    filter_horizontal = ('permisos',)


class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'actividadinicio', 'actividadfin')
    list_filter = ('usuario', 'actividadinicio', 'actividadfin')
    search_fields = ('usuario__username',)
    readonly_fields = ('actividadinicio', 'actividadfin')

admin.site.register(ActividadUsuario, ActividadUsuarioAdmin)