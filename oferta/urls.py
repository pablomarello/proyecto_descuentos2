# oferta/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('crear_oferta/', views.crear_oferta, name='crear_oferta'),
    path('mis_ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),


]
