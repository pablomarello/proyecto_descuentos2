from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView

urlpatterns = [
    path('listado', ProductoListView.as_view(), name='lista_productos'),
    path('crear/', ProductoCreateView.as_view(), name='crear_producto'),
    path('editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),
    path('eliminar/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
]
