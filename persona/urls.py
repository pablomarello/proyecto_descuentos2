from django.urls import path
from . import views

urlpatterns = [
    path('procesar_formulario/', views.procesar_formulario, name='procesar_formulario'),
    path('procesarUsuario/<str:persona_id>/',views.procesarUsuario, name='procesarUsuario')
]