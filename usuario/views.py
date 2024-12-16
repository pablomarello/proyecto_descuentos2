import datetime
from importlib import simple
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import folium.map
from requests import request
from oferente.models import ubicacionesComercio, Oferente
from oferta.models import Oferta, Puntuacion
from producto.models import Categoria, Producto, Subcategoria
from usuario.sms import send_sms
from .forms import LogeoForm
from django.contrib.auth import authenticate,login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UsuarioCreationForm
from django.conf import settings
from persona.models import Persona, ubicaciones
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .email import *
from .models import *
import random
import folium
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Avg
import datetime
from django.db.models import Q, Avg
from django.shortcuts import render, redirect, get_object_or_404
import datetime
from geopy.distance import geodesic
from geopy.distance import distance



def index(request):
    # Consultas generales de ofertas y categorías
    ofertas_vencidas = Oferta.objects.filter(activo=True)
    hoy = datetime.date.today()
    for oferta in ofertas_vencidas:
        if oferta.fecha_fin < hoy:
            oferta.activo = False
            oferta.save()

    baratos = Oferta.objects.filter(activo=True).order_by('precio_oferta')[:5]
    ofertas = Oferta.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    vencen_hoy = Oferta.objects.filter(activo=True, fecha_fin=hoy)

    # Funcionalidad de búsqueda
    query = request.GET.get('q', '').strip()
    if query:
        ofertas = ofertas.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(productos__nombre__icontains=query) |
            Q(productos__categoria__nombre__icontains=query) |
            Q(productos__categoria__categoria__nombre__icontains=query)
        ).distinct()

    # Variables para ubicación y comercios
    ubicacion_usuario = None
    comercios_en_radio = []
    tiene_comercios = False  # Inicialización predeterminada

    if request.user.is_authenticated:
        try:
            persona = request.user.persona_id
            ubicacion_usuario = get_object_or_404(ubicaciones, persona_id=persona)

            lat_usuario = float(ubicacion_usuario.latitud)
            lon_usuario = float(ubicacion_usuario.longitud)

            # Limita la distancia en kilómetros
            radio_km = 100
            ubicaciones_comercio = ubicacionesComercio.objects.filter(comercio_id__habilitado=True)

            for comercio in ubicaciones_comercio:
                if comercio.comercio_id and comercio.comercio_id.nombrecomercio:
                    distancia_km = distance(
                        (lat_usuario, lon_usuario),
                        (float(comercio.latitud), float(comercio.longitud))
                    ).km
                    if distancia_km <= radio_km:
                        comercios_en_radio.append({
                            "id": comercio.comercio_id.id,
                            "nombre": comercio.comercio_id.nombrecomercio,
                            "latitud": float(comercio.latitud),
                            "longitud": float(comercio.longitud),
                        })
            # Verificar si el usuario tiene comercios registrados
            tiene_comercios = Oferente.objects.filter(id_usuario=request.user).exists()
        except ubicaciones.DoesNotExist:
            pass
    else:
        ubicaciones_comercio = ubicacionesComercio.objects.filter(comercio_id__habilitado=True)
        for comercio in ubicaciones_comercio:
            if comercio.comercio_id and comercio.comercio_id.nombrecomercio:
                comercios_en_radio.append({
                    "id": comercio.comercio_id.id,
                    "nombre": comercio.comercio_id.nombrecomercio,
                    "latitud": float(comercio.latitud),
                    "longitud": float(comercio.longitud),
                })

    # Crear lista de ofertas con sus calificaciones
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

    # Renderizado de la plantilla
    return render(request, 'usuarios/ind.html', {
        'categorias': categorias,
        'ofertas_con_calificaciones': ofertas_con_calificaciones,
        'query': query,
       
        'vencen_hoy': vencen_hoy,
        'ubicacion_usuario': {
            'latitud': float(ubicacion_usuario.latitud) if ubicacion_usuario else None,
            'longitud': float(ubicacion_usuario.longitud) if ubicacion_usuario else None,
        } if request.user.is_authenticated else None,
        'comercios_en_radio': comercios_en_radio,
        'usuario_autenticado': request.user.is_authenticated,  # Nuevo parámetro
        'tiene_comercios': tiene_comercios,  # Variable para mostrar botones en el nav en el template
    })



def descuentos_destacados(request):
    # Consultas de ofertas y categorías
    ofertas_vencidas = Oferta.objects.filter(activo=True)
    hoy = datetime.date.today()
    for oferta in ofertas_vencidas:
        # Si la oferta está vencida, desactívala
        if oferta.fecha_fin < hoy:
            oferta.activo = False
            oferta.save()

    ofertas = Oferta.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    vencen_hoy = Oferta.objects.filter(activo=True, fecha_fin=hoy)

    # Aplicar filtros de categorías
    categoria_nombres = request.GET.getlist('category[]')
    if categoria_nombres:
        categoria_ids = Categoria.objects.filter(nombre__in=categoria_nombres).values_list('id', flat=True)
        ofertas = Oferta.objects.filter(productos__categoria__categoria__id__in=categoria_ids, activo=True,eliminado=False)
    else:
        ofertas = Oferta.objects.filter(activo=True,eliminado = False)


    selected_price = request.GET.get('price')  # Obtener el rango de precio seleccionado
    print(f"Rango de precio seleccionado: {selected_price}")

    # Aplicar filtro de precio
    selected_price = request.GET.get('price')
    precio_min = None
    precio_max = None
    if selected_price:
        if selected_price == '10000+':
            precio_min = 10000
        else:
            try:
                min_max = selected_price.split('-')
                precio_min = float(min_max[0])
                precio_max = float(min_max[1]) if len(min_max) > 1 else None
            except ValueError:
                pass
    if precio_min is not None:
        ofertas = ofertas.filter(precio_oferta__gte=precio_min)
    if precio_max is not None:
        ofertas = ofertas.filter(precio_oferta__lte=precio_max)

    # Filtro de ubicación (por distancia máxima desde el usuario)
    ubicacion_usuario = None
    comercios_en_radio = []
    if request.user.is_authenticated:
        try:
            persona = request.user.persona_id
            ubicacion_usuario = get_object_or_404(ubicaciones, persona_id=persona)

            user_lat = float(ubicacion_usuario.latitud)
            user_lon = float(ubicacion_usuario.longitud)

            # Obtener distancias mínimas y máximas
            distance_min_str = request.GET.get('distance_min')
            distance_max_str = request.GET.get('distance_max')
            distance_min = float(distance_min_str) if distance_min_str else 0.0
            distance_max = float(distance_max_str) if distance_max_str else float('inf')

            ofertas_filtradas = []
            for oferta in ofertas:
                ubicacion_comercio = ubicacionesComercio.objects.filter(comercio_id=oferta.oferente).first()
                if ubicacion_comercio and ubicacion_comercio.latitud and ubicacion_comercio.longitud:
                    comercio_coords = (float(ubicacion_comercio.latitud), float(ubicacion_comercio.longitud))
                    distancia_km = distance((user_lat, user_lon), comercio_coords).km
                    if distance_min <= distancia_km <= distance_max:
                        ofertas_filtradas.append(oferta)
                        comercios_en_radio.append({
                            "id": oferta.oferente.id,
                            "nombre": oferta.oferente.nombrecomercio,
                            "latitud": float(ubicacion_comercio.latitud),
                            "longitud": float(ubicacion_comercio.longitud),
                        })
            ofertas = ofertas_filtradas
        except ubicaciones.DoesNotExist:
            pass
    else:
        # Si el usuario no está autenticado, muestra todos los comercios
        ubicaciones_comercio = ubicacionesComercio.objects.all()
        for comercio in ubicaciones_comercio:
            if comercio.comercio_id and comercio.comercio_id.nombrecomercio:
                
                comercios_en_radio.append({
                    "id": comercio.comercio_id.id,
                    "nombre": comercio.comercio_id.nombrecomercio,
                    "latitud": float(comercio.latitud),
                    "longitud": float(comercio.longitud),
                })
    # Calcular calificaciones para ofertas
    ofertas_con_calificaciones = []
    for oferta in ofertas:
        calificaciones = Puntuacion.objects.filter(oferta=oferta)
        cantidad_calificaciones = calificaciones.count()
        calificacion_promedio = calificaciones.aggregate(Avg('calificacion')).get('calificacion__avg', 0) or 0

        ofertas_con_calificaciones.append({
            'oferta': oferta,
            'calificacion_promedio': calificacion_promedio,
            'cantidad_calificaciones': cantidad_calificaciones,
        })

    # Ordenar las ofertas por calificación promedio y limitar a las mejores 3
    ofertas_con_calificaciones = sorted(ofertas_con_calificaciones, key=lambda x: x['calificacion_promedio'], reverse=True)[:5]
    manana = hoy + datetime.timedelta(days=1)
    # Renderizado de la plantilla
    return render(request, 'usuarios/descuento.html', {
        'categorias': categorias,
        'ofertas_con_calificaciones': ofertas_con_calificaciones,
        'vencen_hoy': vencen_hoy,
        'ubicacion_usuario': {
            'latitud': float(ubicacion_usuario.latitud) if ubicacion_usuario else None,
            'longitud': float(ubicacion_usuario.longitud) if ubicacion_usuario else None,
        } if request.user.is_authenticated else None,
        'comercios_en_radio': comercios_en_radio,
        'usuario_autenticado': request.user.is_authenticated,
        'manana':manana,
        'hoy':hoy,
    })

    
""" def descuentos_destacados(request):
    categoria_nombres = request.GET.getlist('category[]')
    print("Nombres de categorías recibidos:", categoria_nombres)  # Verificación
    
    # Obtener los IDs de las categorías a partir de los nombres
    if categoria_nombres:
        categoria_ids = Categoria.objects.filter(nombre__in=categoria_nombres).values_list('id', flat=True)
        print("IDs de categorías obtenidos:", list(categoria_ids))  # Verificación
    else:
        categoria_ids = []
    if categoria_ids:
        ofertas = Oferta.objects.filter(productos__categoria__categoria__id__in=categoria_ids, activo=True)
    else:
        ofertas = Oferta.objects.filter(activo=True)

    # Obtener las ofertas con su calificación promedio
    ofertas_con_calificaciones = []
    for oferta in ofertas:
        calificaciones = Puntuacion.objects.filter(oferta=oferta)
        cantidad_calificaciones = calificaciones.count()
        calificacion_promedio = calificaciones.aggregate(Avg('calificacion')).get('calificacion__avg', 0) or 0

        ofertas_con_calificaciones.append({
            'oferta': oferta,
            'calificacion_promedio': calificacion_promedio,
            'cantidad_calificaciones': cantidad_calificaciones,
        })
    
    # Ordenar las ofertas por calificación promedio
    ofertas_con_calificaciones=sorted(ofertas_con_calificaciones, key=lambda x: x['calificacion_promedio'], reverse=True)[:3]
    
    return render(request, 'usuarios/descuentos.html', {
        'ofertas_con_calificaciones': ofertas_con_calificaciones,
    }) """

def ofertas_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    ofertas = Oferta.objects.filter(productos__categoria__categoria=categoria,activo=True,eliminado=False).distinct()

    # Crear lista de ofertas con sus calificaciones
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

    return render(request, 'usuarios/ind.html', {
        'categoria': categoria,
        'ofertas_con_calificaciones': ofertas_con_calificaciones,
    })


    """ if query:  # Verificar que la consulta no esté vacía
        ofertas = Oferta.objects.filter(activo=True, eliminado= False and
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(productos__nombre__icontains=query) |
            Q(productos__categoria__nombre__icontains=query) |
            Q(productos__categoria__categoria__nombre__icontains=query)
        ).distinct()

    # Crear lista de ofertas con sus calificaciones
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

    return render(request, 'usuarios/ind.html', {
        'query': query,
        'ofertas_con_calificaciones': ofertas_con_calificaciones,
    })
 """
    
    
    
class Index(TemplateView):
    
   template_name='usuarios/index.html'


def mapa(request):
    initial_map=folium.Map(location=[-28.4993802,-65.8233128],zoom_start=5)
    map_html=initial_map._repr_html_()
    context={'map':map_html}
    return render(request, 'usuarios/mapa.html',context)
#Logueo de usuario
#def log(request):
 #   if request.method == 'POST':
  #      username = request.POST['username']
   #     password = request.POST['password']
    #    user = authenticate(request, username=username, password=password)
     #   if user is not None:
      #      login(request, user)
       #     messages.success(request, 'Has iniciado sesión')
        #    return redirect('index')
        #else:
         #   messages.error(request, 'Verifique los datos ingresados')
          #  return redirect('login')
    #else:
     #   return render(request, 'usuarios/login.html')
    
    
#def logout_user(request):
 #   logout(request)
  #  messages.success(request, 'Sesión cerrada')
   # return redirect('logi')





#Creación de usuario y verificacion de email
def generate_verification_token():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def registrar_usuario(request, persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.persona_id = persona

            # Genera token y se guarda en la base de datos
            verification_token = generate_verification_token()
            usuario.token = verification_token
            usuario.save()

            # Si el usuario se está registrando por sí mismo, lo asignamos como usuario_creacion
            usuario.usuario_creacion = usuario
            usuario.save()

            metodo_verificacion = form.cleaned_data['metodo_verificacion']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']
            nombreUsuario=usuario.username
            if metodo_verificacion == 'email':
                # Enviar token por email
                send_email_token(email, usuario.token,nombreUsuario)

            elif metodo_verificacion == 'telefono':
                # Enviar token por SMS
                texto = f'Hola {nombreUsuario} - Ingresa el token de seguridad para completar tu registro: {verification_token}-'
                response_text = send_sms(telefono, texto)
                if "ERROR" in response_text:
                    messages.error(request, f'Error al enviar SMS: {response_text}')
                    return render(request, 'usuarios/registro.html', {'form': form})

            return redirect(reverse('token_input'))
        else:
            messages.error(request, 'Verifique los datos que está ingresando')
    else:
        form = UsuarioCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})



#Verifica el token
def token_input(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            profile = Usuario.objects.get(token=token)
            if profile.token == token:
                profile.is_active = True
                profile.save()
                messages.success(request, 'Tu email ha sido verificado exitosamente')
                return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Error, verifique los datos igresados')
    return render(request, 'usuarios/verificar_token.html')


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        User = get_user_model()
        # Verifica si existe un usuario con el correo electrónico proporcionado
        if User.objects.filter(email=email).exists():
            print('Existe email: '+email)
            # Si existe, envía el correo de restablecimiento de contraseña
            #return super().form_valid(form)
            return super().form_valid(form)
        else:
            # Si no existe, muestra un mensaje de error y redirige a una página de error
            print('No Existe email: '+email)
            #messages.error(self.request, 'No existe una cuenta con este correo electrónico. ' +email)
            #return self.form_invalid(form)
            return redirect('password_reset_error')       
        
#Logueo de usuario

def iniciar_sesion(request):
    # Obtén el valor de `next` desde GET y pásalo al formulario en el contexto
    next_url = request.GET.get('next', reverse('index'))
    
    if request.method == 'POST':
        form = LogeoForm(request.POST)
        if form.is_valid():
            username = request.POST['usuario']
            password = request.POST['contraseña']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige al usuario a la URL de `next` si está presente
                return redirect(request.POST.get('next', reverse('index')))
            else:
                messages.error(request, 'Verifique los datos ingresados')
                return redirect('login')
    else:
        form = LogeoForm()  
    
    return render(request, 'registration/login.html', {'form': form, 'next': next_url})


def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Cerraste la sesión')
    return redirect('login') 

#cambiar contraseña

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('index')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'        

class CustomPasswordResetErrorView(TemplateView):
    template_name = 'registration/password_reset_error.html'    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# Create your views here.
