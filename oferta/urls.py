# oferta/urls.py
from django.urls import path
from . import views
from producto.views import ProductoCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('crear_oferta/', views.crear_oferta, name='crear_oferta'),
    path('mis_ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('recibir_puntuacion/<int:oferta_id>/', views.recibir_puntuacion,name='recibir_puntuacion'),
    path('recibir_comentario/<int:oferta_id>/', views.recibir_comentario,name='recibir_comentario'),
    path('detalle_oferta/<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('oferta/<int:oferta_id>/siguiente/', views.siguiente_oferta, name='siguiente_oferta'),
    path('trazar_ruta/<int:oferta_id>/',views.trazar_ruta, name='trazar_ruta'),
    path('comercios_cercanos/',views.comercios_cercanos, name='comercios_cercanos'),
    path('eliminar_oferta/<int:id_oferta>/',views.eliminar_oferta, name='eliminar_oferta'),
    path('editar_oferta/<int:id_oferta>/',views.editar_oferta,name='editar_oferta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
