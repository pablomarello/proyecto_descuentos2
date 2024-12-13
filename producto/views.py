from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Subcategoria, Categoria
from .forms import ProductoForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

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
    success_url = reverse_lazy('crear_oferta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategorias'] = Subcategoria.objects.filter(eliminado=False) # Pasar las categorías al contexto
        print("Contexto ejecutado:", context['subcategorias'])  # Verifica si se ejecuta
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Agregar un mensaje de éxito
        messages.success(self.request, "El producto se creó exitosamente.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # Agregar un mensaje de error
        messages.error(self.request, "Hubo un error al crear el producto. Por favor, revisa el formulario.")
        return response

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



