from django.urls import path
from . import views

urlpatterns = [
    path("estadisticas/", views.estadisticas_con_graficos, name="estadisticas"),
    path('mapa_calor/',views.mapa_calor_inicio_sesion,name='mapa_calor'),
    path('estadisticas_oferente/',views.estadisticas_oferente, name='estadisticas_oferente'),
]
