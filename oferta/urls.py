# oferta/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_oferta/', views.crear_oferta, name='crear_oferta'),
    path('mis_ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('recibir_puntuacion/<int:oferta_id>/', views.recibir_puntuacion,name='recibir_puntuacion'),
    path('detalle_oferta/<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('trazar_ruta/<int:oferta_id>/',views.trazar_ruta, name='trazar_ruta'),
]


