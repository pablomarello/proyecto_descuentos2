from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registrar',views.registrar_persona, name='registrar_persona'),
    path('mostrar_ubicaciones',views.mostrar_mapa, name='mostrar_ubicaciones'),
    path('registar_ubicacion/<int:persona_id>/',views.registrar_ubicacion,name='registrar_ubicacion'),
    path('ajax/load-provincias/', views.load_provincias, name='ajax_load_provincias'),
    path('ajax/load-deptos/', views.load_deptos, name='ajax_load_deptos'),
    path('ajax/load-municipios/', views.load_municipios, name='ajax_load_municipios'),
    path('ajax/load-localidad/', views.load_localidad, name='ajax_load_localidad'),
    path('ajax/cordenadas_localidades/', views.cordenadas_localidades, name='ajax_cordenadas_localidades'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)