from django.contrib import admin
from persona.models import Persona

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('identificacion','nombres','apellidos') #para listar los campos que queremos que se vean
    
    

admin.site.register(Persona,PersonaAdmin)
# Register your models here.
