from django.urls import path
from .views import verificarCuit, registrarComercio,ubicacion_comercio

urlpatterns = [
    path('verificar_cuit/', verificarCuit, name='verificar_cuit'),
    path('registrar_comercio/', registrarComercio, name='registrar_comercio'),
    path('ubicacion_comercio/<int:comercio_id>', ubicacion_comercio, name= 'ubicacion_comercio'),
]
