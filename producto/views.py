from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Lista de productos (READ)
class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/lista_productos.html'
    context_object_name = 'productos'

# Crear producto (CREATE)
class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/formulario_producto.html'
    success_url = reverse_lazy('lista_productos')

# Actualizar producto (UPDATE)
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/formulario_producto.html'
    success_url = reverse_lazy('lista_productos')

# Eliminar producto (DELETE)
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto/eliminar_producto.html'
    success_url = reverse_lazy('lista_productos')



