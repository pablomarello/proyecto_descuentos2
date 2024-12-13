from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('listado', ProductoListView.as_view(), name='lista_productos'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
