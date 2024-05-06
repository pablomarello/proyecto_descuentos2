from django.contrib import admin
from usuario.models import Usuario, Rol, Personas

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Personas)
# Register your models here.
