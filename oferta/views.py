from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import OfertaForm
from oferta.models import Oferta
from producto.models import Producto
from django.contrib import messages
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse

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





""" def buscar_productos(request):
    query = request.GET.get('query', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:10] 
    resultados = [{'id': producto.id, 'nombre': producto.nombre} for producto in productos]
    return JsonResponse(resultados, safe=False) """

def buscar_productos(request):
    query = request.GET.get('query', '')

    # URL base de la API de Supabase
    supabase_url = 'https://ilwpgwyblwtbcckbxvbt.supabase.co/rest/v1/productos_supabase'
    headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlsd3Bnd3libHd0YmNja2J4dmJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkzNTkzMzAsImV4cCI6MjA0NDkzNTMzMH0.IaXBttzSuqld7EBvv_3d_yrb0lubH8TqnFmmLPVuK6Y',  # Coloca tu API key aquí
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlsd3Bnd3libHd0YmNja2J4dmJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjkzNTkzMzAsImV4cCI6MjA0NDkzNTMzMH0.IaXBttzSuqld7EBvv_3d_yrb0lubH8TqnFmmLPVuK6Y'  # Usa el mismo valor que en 'apikey'
    }

    # Consulta a la API de Supabase filtrando por el nombre del producto
    params = {
        'nombre': f'ilike.%{query}%'  # Filtra usando ilike para búsquedas parciales
    }
    
    # Hacer la solicitud GET a la API
    response = requests.get(supabase_url, headers=headers, params=params)

    if response.status_code == 200:
        # Convertir los datos en JSON
        productos_supabase = response.json()

        # Crear la lista de resultados con id y nombre de cada producto
        resultados = [{'id': producto['id'], 'nombre': producto['nombre']} for producto in productos_supabase]
    else:
        # Si falla la petición, devolvemos una lista vacía
        resultados = []
    
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
        

