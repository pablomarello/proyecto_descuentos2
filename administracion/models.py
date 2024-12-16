from django.db import models
from django.db import models

class ConfiguracionSistema(models.Model):
    cantidad_maxima_ofertas = models.PositiveIntegerField(default=5, verbose_name="Cantidad máxima de ofertas")
    formatos_imagen_permitidos = models.CharField(
        max_length=200, 
        default="jpg,png", 
        verbose_name="Formatos de imagen permitidos",
        help_text="Introduce los formatos separados por comas, por ejemplo: jpg,png"
    )

    def __str__(self):
        return "Configuración del Sistema"



# Create your models here.
