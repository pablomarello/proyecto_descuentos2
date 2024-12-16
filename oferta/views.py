import datetime
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ComentarioForm, OfertaForm
from oferta.models import Comentario, Oferta
from producto.models import Categoria, Producto, Subcategoria
from django.contrib import messages
from django.shortcuts import redirect, render
import requests
from django.http import JsonResponse
import folium
from .forms import OfertaForm
from oferta.models import Oferta, Puntuacion
from producto.models import Producto
from django.contrib import messages
from django.shortcuts import redirect, render
import requests

from oferta.models import Puntuacion
from django.db.models import Avg
from django.http import HttpResponse,JsonResponse
from persona.models import ubicaciones
from oferente.models import ubicacionesComercio
from geopy.distance import distance

from datetime import datetime, date 
from administracion.models import ConfiguracionSistema



        

def comercios_cercanos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Primero debes iniciar sesión')
        return redirect('login')
    
    ofertas = Oferta.objects.filter(activo=True)
    baratos = Oferta.objects.filter(activo=True).order_by('precio_oferta')[:5]
    hoy = datetime.date.today()
    categorias = Categoria.objects.all()
    vencen_hoy = Oferta.objects.filter(activo=True, fecha_fin=hoy)
    

    # Crear lista de ofertas con sus calificaciones
    

    persona = request.user.persona_id
    ubicacion_usuario = get_object_or_404(ubicaciones, persona_id=persona)

    lat_usuario = float(ubicacion_usuario.latitud)
    lon_usuario = float(ubicacion_usuario.longitud)
    
    #LIMITA LA DISTACIA EN KILOMETROS
    radio_km = 100

    ubicaciones_comercio = ubicacionesComercio.objects.all()

    comercios_en_radio = []
    
    for comercio in ubicaciones_comercio:
        if comercio.comercio_id and comercio.comercio_id.nombrecomercio:
            distancia_km = distance((lat_usuario, lon_usuario), 
                                    (float(comercio.latitud), float(comercio.longitud))).km
            if distancia_km <= radio_km:
                comercios_en_radio.append({
                    "nombre": comercio.comercio_id.nombrecomercio,
                    "latitud": float(comercio.latitud),
                    "longitud": float(comercio.longitud),
                })

    ofertas_con_calificaciones = []
    for oferta in ofertas:
        calificaciones = Puntuacion.objects.filter(oferta=oferta)
        cantidad_calificaciones = calificaciones.count()
        calificacion_promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg'] or 0

        ofertas_con_calificaciones.append({
            'oferta': oferta,
            'calificacion_promedio': calificacion_promedio,
            'cantidad_calificaciones': cantidad_calificaciones,
        })

    context = {
        'ubicacion_usuario': {'latitud': lat_usuario, 'longitud': lon_usuario},
        'comercios_en_radio': comercios_en_radio,
    }

    return render(request, 'oferta/comercios_cercanos.html', context)


def trazar_ruta(request, oferta_id):
    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        messages.error(request, 'Primero debes iniciar sesión')
        return redirect('login')


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
        return redirect('detalle_oferta', oferta_id=oferta_id)

    # Si no es POST, redirige a la página de detalles de la oferta
    return redirect('detalle_oferta', oferta_id=oferta_id)


def recibir_comentario(request, oferta_id):
    # Verifica si el método es POST
    if request.method == 'POST':
        oferta = get_object_or_404(Oferta, id=oferta_id)
        comentario = request.POST.get('comentario')

        # Verifica si ya ha comentado esta oferta
        comentario_existente = Comentario.objects.filter(oferta=oferta, usuario=request.user).exists()

        if not comentario_existente:
            # Crea una nuevo comentario 
            Comentario.objects.create(
                oferta=oferta,
                usuario=request.user,  # Campo 'usuario' en lugar de 'user'
                comentario=comentario  # Campo 'estrellas' en lugar de 'puntuacion'
            )
        
        # Redirige a la página de detalles de la oferta después de votar
        return redirect('detalle_oferta', oferta_id=oferta_id)

    # Si no es POST, redirige a la página de detalles de la oferta
    return redirect('detalle_oferta', oferta_id=oferta_id)




def detalle_oferta(request, oferta_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Inicia sesión para ver los detalles de cada oferta')
        # Redirige al usuario a la página de inicio de sesión, pasando la URL actual como `next`
        login_url = f"{reverse('login')}?next={request.path}"
        return redirect(login_url)

    oferta = get_object_or_404(Oferta, id=oferta_id)
    
    # Obtener ubicación del usuario
    persona = request.user.persona_id
    ubicacion_persona = get_object_or_404(ubicaciones, persona_id=persona)

    # Obtener ubicación del comercio
    oferente = oferta.oferente
    try:
        ubicacion_comercio = ubicacionesComercio.objects.get(comercio_id=oferente.id)
    except ubicacionesComercio.DoesNotExist:
        return HttpResponse("No se encontró la ubicación del comercio para la oferta proporcionada.", status=404)

    # Convertir ubicaciones a formato JSON
    ubicacion_usuario = {
        'latitud': float(ubicacion_persona.latitud),
        'longitud': float(ubicacion_persona.longitud)
    }
    ubicacion_comercio_data = {
        'latitud': float(ubicacion_comercio.latitud),
        'longitud': float(ubicacion_comercio.longitud)
    }
    
    # Verificar si el usuario ha votado
    user_ha_votado = False
    if request.user.is_authenticated:
        user_ha_votado = Puntuacion.objects.filter(oferta=oferta, usuario=request.user).exists()
    
    # Obtener calificación promedio
    comentarios=Comentario.objects.filter(oferta=oferta)
    
    calificaciones = Puntuacion.objects.filter(oferta=oferta)
    cantidad_calificaciones=calificaciones.count()
    calificacion_promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    # Verificar si el usuario ya hizo un comentario en esta oferta
    puede_comentar = not Comentario.objects.filter(oferta=oferta, usuario=request.user).exists()
    # Inicializar el formulario de comentarios
    # Obtener comentarios junto con sus puntuaciones
    comentarios_con_puntuacion = []
    comentarios = Comentario.objects.filter(oferta=oferta)

    for comentario in comentarios:
        # Obtener la puntuación del usuario para la oferta específica, si existe
        puntuacion_usuario = Puntuacion.objects.filter(oferta=oferta, usuario=comentario.usuario).first()
        comentarios_con_puntuacion.append({
            'comentario': comentario,
            'puntuacion': puntuacion_usuario.calificacion if puntuacion_usuario else None
        })

    # Inicializar el formulario de comentarios
    comentario_form = ComentarioForm()
    
    # Pasar la información al contexto
    context = {
        'oferta': oferta,
        'user_ha_votado': user_ha_votado,
        'comentarios_con_puntuacion': comentarios_con_puntuacion,
        'calificacion_promedio': calificacion_promedio,
        'cantidad_calificaciones': cantidad_calificaciones,
        'ubicacion_usuario': json.dumps(ubicacion_usuario),
        'ubicacion_comercio': json.dumps(ubicacion_comercio_data),
        'puede_comentar': puede_comentar,
        'comentario_form': comentario_form
    }
    return render(request, 'oferta/detalle_oferta.html', context)

def siguiente_oferta(request, oferta_id):
    # Obtener la oferta actual
    oferta_actual = get_object_or_404(Oferta, id=oferta_id)
    
    # Obtener la siguiente oferta en orden de id o alguna otra lógica
    siguiente = Oferta.objects.filter(id__gt=oferta_actual.id).order_by('id').first()
    
    # Si existe una siguiente oferta, redirigir a su detalle
    if siguiente:
        return redirect('detalle_oferta', oferta_id=siguiente.id)
    else:
        # Si no hay siguiente, redirigir a la primera oferta como bucle
        primera_oferta = Oferta.objects.order_by('id').first()
        return redirect('detalle_oferta', oferta_id=primera_oferta.id)


def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES, user=request.user)
        
        # Obtener los IDs de productos seleccionados y eliminar cualquier valor vacío
        productos_ids = request.POST.get('productos_seleccionados', '').split(',')
        productos_ids = [id for id in productos_ids if id]  # Filtrar valores vacíos
        
        
    # Aquí puedes agregar los mensajes de error personalizados de validación si necesitas
        if 'imagen' in form.errors:
            messages.error(request, form.errors['imagen'][0])  # Mostrar el error de imagen

        if not productos_ids:
            messages.error(request, "La oferta debe contener al menos 1 producto.")
        elif form.is_valid():
            # Obtener el comercio seleccionado
            oferente = form.cleaned_data['oferente']
            
            # Obtener el CUIT del oferente
            cuit_oferente = oferente.cuit
            
            # Filtrar ofertas del mismo CUIT
            ofertas_del_oferente = Oferta.objects.filter(oferente__cuit=cuit_oferente,activo=True,eliminado=False)
            
            
            config = ConfiguracionSistema.objects.first()
            print(config.cantidad_maxima_ofertas,'  cantidad max')
            # Comparar la cantidad de ofertas con la máxima permitida
            if ofertas_del_oferente.count() >= config.cantidad_maxima_ofertas:
                print ('Entró al if xD')
                
                messages.warning(request, f'Alcanzaste el máximo de ofertas permitidas para tu plan')
                return redirect('mis_ofertas')
            
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

""" def buscar_productos(request):
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
 """




def mis_ofertas(request):
    # Obtén el usuario actual
    hoy = date.today()
    user = request.user
    
    # Filtra las ofertas por los comercios que pertenecen al usuario
    ofertas_vencidas = Oferta.objects.filter(oferente__id_usuario=user)
    for oferta in ofertas_vencidas:
        # Si la oferta está vencida, desactívala
        if oferta.fecha_fin < hoy:
            oferta.activo = False
            oferta.save()
    
    ofertas = Oferta.objects.filter(oferente__id_usuario=user, eliminado=False)
    
    return render(request, 'oferta/mis_ofertas.html', {'ofertas': ofertas, 'hoy':hoy})

def editar_oferta(request,id_oferta):
    oferta = get_object_or_404(Oferta, id=id_oferta)
    
    if request.method == 'POST':
        oferta.titulo = request.POST.get('titulo')
        oferta.descripcion = request.POST.get('descripcion')
        oferta.precio_normal = request.POST.get('precio_normal')
        oferta.precio_oferta = request.POST.get('precio_oferta')
        oferta.fecha_inicio = request.POST.get('fecha_inicio')
        oferta.fecha_fin = request.POST.get('fecha_fin')
        
        hoy = date.today()

        # Validar fechas
        if oferta.fecha_inicio and oferta.fecha_fin:
            # Convertir las fechas a objetos datetime.date para comparación
            fecha_inicio = datetime.strptime(oferta.fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(oferta.fecha_fin, '%Y-%m-%d').date()

            # Validar que las fechas no sean anteriores a hoy
            if fecha_inicio < hoy:
                messages.error(request, "La fecha de inicio no puede ser anterior a hoy.")
                return render(request, 'oferta/editar_oferta.html', {'oferta': oferta})

            if fecha_fin < hoy:
                messages.error(request, "La fecha de fin no puede ser anterior a hoy.")
                return render(request, 'oferta/editar_oferta.html', {'oferta': oferta})

            # Validar que la fecha de inicio no sea posterior a la fecha de fin
            if fecha_inicio > fecha_fin:
                messages.error(request, "La fecha de inicio no puede ser posterior a la fecha de fin.")
                return render(request, 'oferta/editar_oferta.html', {'oferta': oferta})
        
        # Si hay una nueva imagen, actualizarla
        if request.FILES.get('imagen'):
            oferta.imagen = request.FILES['imagen']
            
        
        oferta.activo = True
        oferta.save()
        
        messages.success(request, "La oferta ha sido actualizada correctamente.")
        return redirect('mis_ofertas')
    
    return render(request, 'oferta/editar_oferta.html', {'oferta': oferta})

def eliminar_oferta(request,id_oferta):
    if request.method == "POST":
        # Obtiene la oferta o muestra un error 404 si no existe
        oferta = get_object_or_404(Oferta, pk = id_oferta)
        
        # Elimina la oferta
        oferta.eliminado=True
        oferta.save()
        
        # Agrega un mensaje de éxito (opcional)
        messages.success(request, "La oferta ha sido eliminada exitosamente.")
        
        # Redirige a la página de las ofertas
        return redirect('mis_ofertas')
    else:
        # Si no es un método POST, redirige a la página de ofertas
        return redirect('mis_ofertas')


def ofertas(request):
    ofertas = Oferta.objects.filter(activo=True)
    
    return render(request, 'index.html', {'ofertas':ofertas })
        

