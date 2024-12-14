from django.urls import path
from . import views

urlpatterns = [
    path('login_superuser', views.login_superuser, name='login_superuser'),
    path('',views.index_admin, name='index_admin'),
    path('logout/', views.logout_superuser, name='logout_superuser'),
    path('usuarios_admin',views.usuarios_admin , name='usuarios_admin'),
    path('editar_usuario/<int:id_usuario>/',views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:id_usuario>/',views.eliminar_usuario, name='eliminar_usuario'),
    path('comercios_admin',views.comercios_admin , name='comercios_admin'),
    path('editar_comercio/<int:id_comercio>/',views.editar_comercio, name='editar_comercio'),
    path('eliminar_comercio/<int:id_comercio>/',views.eliminar_comercio, name='eliminar_comercio'),
    path('ofertas_admin',views.ofertas_admin , name='ofertas_admin'),
    path('editar_oferta_admin/<int:id_oferta>/',views.editar_oferta_admin,name='editar_oferta_admin'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle_oferente_status/<int:user_id>/', views.toggle_oferente_status, name='toggle_oferente_status'),
    path('toggle_oferta_status/<int:user_id>/', views.toggle_oferta_status, name='toggle_oferta_status'),
    
    path("estadisticas/", views.estadisticas_con_graficos, name="estadisticas"),
    path('mapa_calor/',views.mapa_calor_inicio_sesion,name='mapa_calor'),
    

]
