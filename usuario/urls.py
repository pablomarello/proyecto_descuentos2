"""
URL configuration for proyecto_descuentos2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
<<<<<<< HEAD
from usuario.views import Index

urlpatterns = [
   
    path('',Index.as_view(), name='index'),
=======
from usuario import views

urlpatterns = [
    path('procesarUsuario/<str:identificacion>/', views.procesarUsuario, name='procesarUsuario'),
    path('formulario_exitoso/', views.formulario_exitoso, name='formulario_exitoso'),
>>>>>>> parent of 608f4b1 (cambio de contraseña e inicio de sesion)
]
