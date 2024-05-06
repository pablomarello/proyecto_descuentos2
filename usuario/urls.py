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
from usuario import views
from usuario.views import Index
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('procesarUsuario/<str:identificacion>/', views.procesarUsuario, name='procesarUsuario'),
    path('formulario_exitoso/', views.formulario_exitoso, name='formulario_exitoso'),
    path('login/',views.login,name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    #CAMBIO DE CONTRASEÑA
    path('reset_password/', PasswordResetView.as_view(),{'template_name':'registration/password_reset_form.html','email_template':'registration/password_reset_email.html'}, name='reset_password'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
