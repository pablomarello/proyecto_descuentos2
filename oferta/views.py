import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OfertaForm
from oferta.models import Oferta
from producto.models import Producto
from django.contrib import messages
import folium

from oferta.models import Oferta, Puntuacion
from producto.models import Producto
from django.contrib import messages
import requests
from django.http import JsonResponse
from oferta.models import Puntuacion
from django.db.models import Avg
from django.http import HttpResponse,JsonResponse
from persona.models import ubicaciones
from oferente.models import ubicacionesComercio
from geopy.distance import distance

def trazar_ruta(request, oferta_id):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        return HttpResponse("Usuario no autenticado.")

    # Obtén la ubicación del usuario
    persona = request.user.persona_id
    ubicacion_persona = get_object_or_404(ubicaciones, persona_id=persona)

    # Obtén la oferta y su oferente
    oferta = get_object_or_404(Oferta, id=oferta_id)
    oferente = oferta.oferente

    # Busca la ubicación del oferente en ubicacionesComercio
    try:
        ubicacion_comercio = ubicacionesComercio.objects.get(comercio_id=oferente.id)
    except ubicacionesComercio.DoesNotExist:
        return HttpResponse("No se encontró la ubicación del comercio para la oferta proporcionada.", status=404)

    # Convierte los valores Decimal a float para evitar errores de serialización
    ubicacion_usuario = {
        'latitud': float(ubicacion_persona.latitud),
        'longitud': float(ubicacion_persona.longitud)
    }
    ubicacion_comercio_data = {
        'latitud': float(ubicacion_comercio.latitud),
        'longitud': float(ubicacion_comercio.longitud)
    }

    # Renderiza el template con los datos serializados
    return render(request, 'oferta/ruta_comercio.html', {
        'ubicacion_usuario': json.dumps(ubicacion_usuario),
        'ubicacion_comercio': json.dumps(ubicacion_comercio_data)
    })
    





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

""" def ofertas(request):
    ofertas = Oferta.objects.filter(activo=True)
    
    return render(request, 'index.html', {'ofertas':ofertas }) """
        

def recibir_puntuacion(request, oferta_id):
    # Verifica si el método es POST
    if request.method == 'POST':
        oferta = get_object_or_404(Oferta, id=oferta_id)
        calificacion = request.POST.get('estrellas')

        # Verifica si ya ha puntuado esta oferta
        puntuacion_existente = Puntuacion.objects.filter(oferta=oferta, usuario=request.user).exists()

        if not puntuacion_existente:
            # Crea una nueva puntuación utilizando los campos correctos
            Puntuacion.objects.create(
                oferta=oferta,
                usuario=request.user,  # Campo 'usuario' en lugar de 'user'
                calificacion=calificacion  # Campo 'estrellas' en lugar de 'puntuacion'
            )
        
        # Redirige a la página de detalles de la oferta después de votar
        return redirect('index')

    # Si no es POST, redirige a la página de detalles de la oferta
    return redirect('detalle_oferta', oferta_id=oferta_id)


def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    # Verificar si el usuario ha votado
    user_ha_votado = False
    if request.user.is_authenticated:
        user_ha_votado = Puntuacion.objects.filter(oferta=oferta, usuario=request.user).exists()
    
    # Obtener calificación promedio
    calificaciones = Puntuacion.objects.filter(oferta=oferta)
    cantidad_calificaciones=calificaciones.count()
    calificacion_promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    
    
    print("Esta es la califiiicacion ",calificacion_promedio)
    print("Esta es la cantidad ",cantidad_calificaciones)
    
    
    context = {
        'oferta': oferta,
        'user_ha_votado': user_ha_votado,
        'calificacion_promedio': calificacion_promedio,
        'cantidad_calificaciones':cantidad_calificaciones
    }
    
    
    return render(request, 'oferta/detalle_oferta.html', context)