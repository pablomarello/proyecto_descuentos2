from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import OfertaForm
from oferta.models import Oferta
from producto.models import Producto
from django.contrib import messages
from django.shortcuts import redirect, render

def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST, user=request.user)
        
        # Obtener los IDs de productos seleccionados y eliminar cualquier valor vacío
        productos_ids = request.POST.get('productos_seleccionados', '').split(',')
        productos_ids = [id for id in productos_ids if id]  # Filtrar valores vacíos

        if not productos_ids:
            messages.error(request, "La oferta debe contener al menos 1 producto.")
        elif form.is_valid():
            oferta = form.save(commit=False)  # Guardamos el objeto sin guardarlo aún en la base de datos
            oferta.save()  # Guardamos la oferta en la base de datos

            # Asociar los productos a la oferta
            productos = Producto.objects.filter(id__in=productos_ids)
            oferta.productos.set(productos)  # Asignar los productos a la oferta

            return redirect('mis_ofertas')  
    else:
        form = OfertaForm(user=request.user)

    return render(request, 'oferta/crear_oferta.html', {'form': form})





def buscar_productos(request):
    query = request.GET.get('query', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:10] 
    resultados = [{'id': producto.id, 'nombre': producto.nombre} for producto in productos]
    return JsonResponse(resultados, safe=False)


def mis_ofertas(request):
    # Obtén el usuario actual
    user = request.user
    
    # Filtra las ofertas por los comercios que pertenecen al usuario
    ofertas = Oferta.objects.filter(oferente__id_usuario=user)
    
    return render(request, 'oferta/mis_ofertas.html', {'ofertas': ofertas})

def ofertas(request):
    ofertas = Oferta.objects.filter(activo=True)
    
    return render(request, 'index.html', {'ofertas':ofertas })
        

