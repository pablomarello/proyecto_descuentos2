from django.urls import path
from . import views

urlpatterns = [
    path('login_superuser', views.login_superuser, name='login_superuser'),
    path('',views.index_admin, name='index_admin'),
    path('logout/', views.logout_superuser, name='logout_superuser'),
    path('usuarios_admin',views.usuarios_admin , name='usuarios_admin'),
    path('registrar_usuario_admin/', views.registrar_usuario_admin, name='registrar_usuario_admin'),
    path('registrar_usuario_admin/<int:persona_id>/', views.registrar_usuario_admin, name='registrar_usuario_admin'),
    path('crear_superusuario/', views.crear_superusuario, name='crear_superusuario'),

    path('editar_usuario/<int:id_usuario>/',views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:id_usuario>/',views.eliminar_usuario, name='eliminar_usuario'),
    path('comercios_admin',views.comercios_admin , name='comercios_admin'),
    path('editar_comercio/<int:id_comercio>/',views.editar_comercio, name='editar_comercio'),
    path('eliminar_comercio/<int:id_comercio>/',views.eliminar_comercio, name='eliminar_comercio'),
    path('ofertas_admin',views.ofertas_admin , name='ofertas_admin'),
    path('editar_oferta_admin/<int:id_oferta>/',views.editar_oferta_admin,name='editar_oferta_admin'),
    path('eliminar_oferta_admin/<int:id_oferta>/',views.eliminar_oferta_admin,name='eliminar_oferta_admin'),
    path('productos_admin',views.productos_admin , name='productos_admin'),
    path('editar_producto_admin/<int:id_producto>/',views.editar_producto_admin,name='editar_producto_admin'),
    path('eliminar_producto_admin/<int:id_producto>/',views.eliminar_producto_admin,name='eliminar_producto_admin'),
    path('categorias_admin',views.categorias_admin , name='categorias_admin'),
    path('editar_categoria_admin/<int:id_categoria>/',views.editar_categoria_admin, name='editar_categoria_admin'),
    path('eliminar_categoria_admin/<int:id_categoria>/',views.eliminar_categoria_admin,name='eliminar_categoria_admin'),
    path('subcategorias_admin',views.subcategorias_admin , name='subcategorias_admin'),
    path('editar_subcategoria_admin/<int:id_subcategoria>/',views.editar_subcategoria_admin,name='editar_subcategoria_admin'),
    path('eliminar_subcategoria_admin/<int:id_subcategoria>/',views.eliminar_subcategoria_admin,name='eliminar_subcategoria_admin'),
    path('personas_admin',views.personas_admin , name='personas_admin'),
    path('editar_persona_admin/<int:identificacion>/', views.editar_persona_admin, name='editar_persona_admin'),

    path('eliminar_persona_admin/<int:identificacion>/',views.eliminar_persona_admin,name='eliminar_persona_admin'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle_oferente_status/<int:user_id>/', views.toggle_oferente_status, name='toggle_oferente_status'),
    path('toggle_oferta_status/<int:user_id>/', views.toggle_oferta_status, name='toggle_oferta_status'),
    path('toggle_persona_status/<int:identificacion>/', views.toggle_persona_status, name='toggle_persona_status'),
    path('auditoria_admin',views.auditoria_admin , name='auditoria_admin'),
    path('auditoria_admin/usuarios',views.auditoria_usuarios , name='auditoria_usuarios'),
    path('auditoria_admin/personas',views.auditoria_personas , name='auditoria_personas'),
    path('auditoria_admin/ofertas',views.auditoria_ofertas , name='auditoria_ofertas'),
    path('auditoria_admin/comercios',views.auditoria_comercios , name='auditoria_comercios'),
    path('auditoria_admin/productos',views.auditoria_productos , name='auditoria_productos'),
    path('auditoria_admin/categorias',views.auditoria_categorias , name='auditoria_categorias'),
    path('auditoria_admin/subcategorias',views.auditoria_subcategorias , name='auditoria_subcategorias'),
    
    path("configurar_sistema/", views.configurar_sistema, name="configurar_sistema"),
    path("estadisticas/", views.estadisticas_con_graficos, name="estadisticas"),
    path('mapa_calor/',views.mapa_calor_inicio_sesion,name='mapa_calor'),
    

]
