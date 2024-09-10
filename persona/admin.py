from django.contrib import admin
from persona.models import Persona, ubicaciones,TablaDepartamento,TablaMunicipio,TablaLocalidad,TablaPais,TablaProvincia

class TablaPaisAdmin(admin.ModelAdmin):
    search_fields = ['nom_pais']

class TablaProvinciaAdmin(admin.ModelAdmin):
    search_fields = ['nom_pcia']

class TablaDepartamentoAdmin(admin.ModelAdmin):
    search_fields = ['nom_depto']

class TablaMunicipioAdmin(admin.ModelAdmin):
    search_fields = ['nom_agl']

class TablaLocalidadAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


class PersonaAdmin(admin.ModelAdmin):
    list_display = ('identificacion','nombres','apellidos') #para listar los campos que queremos que se vean
    search_fields=['nombres']
    
class ubicacionesAdmin(admin.ModelAdmin):
    ordering=['pais']
    autocomplete_fields=['pais','provincia','departamento','municipio','localidad']
    
admin.site.register(Persona,PersonaAdmin)
admin.site.register(ubicaciones,ubicacionesAdmin)
admin.site.register(TablaPais,TablaPaisAdmin)
admin.site.register(TablaProvincia,TablaProvinciaAdmin)
admin.site.register(TablaDepartamento,TablaDepartamentoAdmin)
admin.site.register(TablaMunicipio,TablaMunicipioAdmin)
admin.site.register(TablaLocalidad,TablaLocalidadAdmin)
# Register your models here.
