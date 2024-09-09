from django.urls import path
from .views import verificarCuit, registrarComercio

urlpatterns = [
    path('verificar_cuit/', verificarCuit, name='verificar_cuit'),
    path('registrar_comercio/', registrarComercio, name='registrar_comercio'),
]
