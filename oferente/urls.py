from django.urls import path
from .views import comercios, verificarCuit, registrarComercio,ubicacion_comercio, lista_comercio, perfil_comercio

urlpatterns = [
    path('verificar_cuit/', verificarCuit, name='verificar_cuit'),
    path('registrar_comercio/', registrarComercio, name='registrar_comercio'),
    path('ubicacion_comercio/<int:comercio_id>', ubicacion_comercio, name= 'ubicacion_comercio'),
    path('lista_comercios/', lista_comercio, name= 'lista_comercios'),
    path('perfil_comercio/<int:comercio_id>/', perfil_comercio, name= 'perfil_comercio'),
    path('comercios/', comercios, name='comercios'),
]
