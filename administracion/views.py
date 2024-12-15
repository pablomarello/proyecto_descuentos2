from datetime import date, datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import ComercioForm, UsuarioForm, OfertaForm
from usuario.models import Usuario
from oferta.models import Oferta
from oferente.models import Oferente, ubicacionesComercio
from persona.models import Persona
from producto.models import Producto, Categoria, Subcategoria
from .forms import PersonForm

#LOGUEO ADMIN
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginSuperuserForm
from django.contrib.auth.decorators import login_required







def login_superuser(request):
    print('1')
    if request.method == 'POST':
        print('2')
        form = LoginSuperuserForm(request.POST)
        if form.is_valid():
            print('3')
            user = form.cleaned_data['user']
            print('4')
            login(request, user)
            print('Si funciona xD')
            messages.success(request, f"Bienvenido, {user.username}")
            return redirect('index_admin')  # Cambia a la vista principal del panel
    else:
        form = LoginSuperuserForm()
    return render(request, 'administracion/login_admin.html', {'form': form})


def logout_superuser(request):
    logout(request)
    messages.success(request, "Cerraste la sesión")
    return redirect('login_superuser')





# Create your views here.

def index_admin(request):
    return render(request,'administracion/base_admin.html')
    

#AGREGAR, EDITAR, ELIMINAR USUARIOS

#funcion manejando la persona desde el forms
def registrar_usuario_admin(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios_admin')  # Redirige tras registrar
    else:
        form = UsuarioForm()
    return render(request, 'administracion/registro_usuario_admin.html', {'form': form})


#funcion mandando el contexto de persona al formulario
""" def registrar_usuario_admin(request, persona_id=None):
    if persona_id:
        # Lógica cuando se proporciona persona_id
        persona = get_object_or_404(Persona, id=persona_id)
    else:
        persona = None  # O redirigir si persona_id es obligatorio

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        persona_id = request.POST.get('persona_id')  # Recupera el ID de la persona seleccionada
        persona = get_object_or_404(Persona, id=persona_id)  # Asegúrate de que exista

        if form.is_valid():
            usuario = form.save(commit=False)
            if persona:
                usuario.persona_id = persona
            usuario.save()
            return redirect('usuarios_admin')  # Redirige tras registrar
    else:
        form = UsuarioForm()
        personas = Persona.objects.filter(usuario__isnull=True, eliminado=False)  # Pasa las personas al contexto para el select
    return render(request, 'administracion/registro_usuario_admin.html', {'form': form, 'personas': personas}) """


def usuarios_admin(request):
    """ # Manejo del formulario al enviar datos
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios')
        else:
            messages.error(request, 'Error al crear el usuario. Verifica los datos ingresados.')
            print(form.errors) 
            form = UsuarioCreationForm()  # Crea una nueva instancia del formulario """

    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'username')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        usuarios = Usuario.objects.filter(username__icontains=search_query, is_active=True)
    else:
        usuarios = Usuario.objects.all()

    # Ordenar usuarios por el parámetro recibido
    usuarios = usuarios.order_by(order)

    """  paginator = Paginator(usuarios, 8)  # Paginamos con 8 usuarios por página
        page_number = request.GET.get('page')  # Obtiene el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página actual """

    return render(request, 'administracion/usuarios_admin.html', {
        
        'usuarios':usuarios,
        'search_query': search_query,
        'order': order,
    })
    
def editar_usuario(request, id_usuario):
    # Obtener el objeto de insumo a editar
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    
    
    if request.method == 'POST':
        # Pasar la instancia existente al formulario para editar
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request,f'El usuario: {usuario.username} fué editado.')

            # Redirigir a la lista de usuarios correctamente
            return redirect('usuarios_admin')
    else:
        # Si no es POST, mostrar el formulario con los datos existentes del insumo
        form = UsuarioForm(instance=usuario)
    
    # Renderizar el formulario de edición
    return render(request, 'administracion/editar_usuario.html', {'form': form, 'usuario': usuario})    



def eliminar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    # Verificar si el usuario está intentando eliminarse a sí mismo
    if request.user.id == usuario.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('usuarios_admin')

    if request.method == 'POST':
        usuario.is_active = False  # Eliminación lógica (desactivación)
        usuario.eliminado = True
        usuario.save()
        messages.success(request, f'El usuario "{usuario.username}" ha sido eliminado exitosamente.')
        return redirect('usuarios_admin')

    return redirect('usuarios_admin')
    
    
#AGREGAR, EDITAR, ELIMINAR COMERCIOS
def comercios_admin(request):
    """ # Manejo del formulario al enviar datos
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios')
        else:
            messages.error(request, 'Error al crear el usuario. Verifica los datos ingresados.')
            print(form.errors) 
            form = UsuarioCreationForm()  # Crea una nueva instancia del formulario """

    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'nombrecomercio')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        comercios = Oferente.objects.filter(nombrecomercio=search_query)
    else:
        comercios = Oferente.objects.all().select_related('ubicacionescomercio').order_by('nombrecomercio')


    # Ordenar usuarios por el parámetro recibido
    comercios = comercios.order_by(order)

    """ paginator = Paginator(comercios, 8)  # Paginamos con 8 usuarios por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual """

    return render(request, 'administracion/comercios_admin.html', {
        'comercios':comercios,
        'search_query': search_query,
        'order': order,
    })
    
    
def editar_comercio(request, id_comercio):
    # Obtener el objeto de insumo a editar
    comercio = get_object_or_404(Oferente, pk=id_comercio)
    
    if request.method == 'POST':
        # Pasar la instancia existente al formulario para editar
        form = ComercioForm(request.POST, instance=comercio)
        if form.is_valid():
            form.save()
            messages.success(request,f'El comercio: {comercio.nombrecomercio} fué editado.')

            # Redirigir a la lista de usuarios correctamente
            return redirect('comercios_admin')
    else:
        # Si no es POST, mostrar el formulario con los datos existentes del insumo
        form = ComercioForm(instance=comercio)
    
    # Renderizar el formulario de edición
    return render(request, 'administracion/editar_comercio.html', {'form': form, 'oferente': comercio})    



def eliminar_comercio(request, id_comercio):
    comercio = get_object_or_404(Oferente, pk=id_comercio)

    if request.method == 'POST':
        comercio.habilitado = False  # Eliminación lógica (desactivación)
        comercio.eliminado = True
        comercio.save()
        messages.success(request, f'El usuario "{comercio.nombrecomercio}" ha sido eliminado exitosamente.')
        return redirect('comercios_admin')

    return redirect('comercio_admin')
    
    


    
#AGREGAR, EDITAR, ELIMINAR COMERCIOS
def ofertas_admin(request):
    """ # Manejo del formulario al enviar datos
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios')
        else:
            messages.error(request, 'Error al crear el usuario. Verifica los datos ingresados.')
            print(form.errors) 
            form = UsuarioCreationForm()  # Crea una nueva instancia del formulario """

    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'titulo')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        ofertas = Oferta.objects.filter(titulo=search_query)
    else:
        ofertas = Oferta.objects.all()

    # Ordenar usuarios por el parámetro recibido
    ofertas = ofertas.order_by(order)

    """ paginator = Paginator(ofertas, 8)  # Paginamos con 8 usuarios por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual """

    return render(request, 'administracion/ofertas_admin.html', {
        'ofertas':ofertas,
        
        'search_query': search_query,
        'order': order,
    })
    
    
    
def editar_oferta_admin(request,id_oferta):
    oferta = get_object_or_404(Oferta, id=id_oferta)
    
    if request.method == 'POST':
        oferta.titulo = request.POST.get('titulo')
        oferta.descripcion = request.POST.get('descripcion')
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
                return render(request, 'administracion/editar_oferta.html', {'oferta': oferta})

            if fecha_fin < hoy:
                messages.error(request, "La fecha de fin no puede ser anterior a hoy.")
                return render(request, 'administracion/editar_oferta.html', {'oferta': oferta})

            # Validar que la fecha de inicio no sea posterior a la fecha de fin
            if fecha_inicio > fecha_fin:
                messages.error(request, "La fecha de inicio no puede ser posterior a la fecha de fin.")
                return render(request, 'administracion/editar_oferta.html', {'oferta': oferta})
        
        # Si hay una nueva imagen, actualizarla
        if request.FILES.get('imagen'):
            oferta.imagen = request.FILES['imagen']
        
        oferta.save()
        
        messages.success(request, "La oferta ha sido actualizada correctamente.")
        return redirect('ofertas_admin')
    
    return render(request, 'administracion/editar_oferta.html', {'oferta': oferta})

def eliminar_oferta_admin(request, id_oferta):
    oferta = get_object_or_404(Oferta, id=id_oferta)

    if request.method == 'POST':
        oferta.activo = False
        oferta.eliminado = True
        oferta.save()
        messages.success(request, f'La oferta "{oferta.titulo}" ha sido eliminada exitosamente.')
        return redirect('ofertas_admin')
    return redirect('ofertas_admin')


def productos_admin(request):
    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'nombre')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        productos = Producto.objects.filter(nombre=search_query)
    else:
        productos = Producto.objects.all()

    # Ordenar usuarios por el parámetro recibido
    productos = productos.order_by(order)

    return render(request, 'administracion/productos_admin.html', {
        'productos':productos,
        
        'search_query': search_query,
        'order': order,
    })

def editar_producto_admin(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    subcategorias = Subcategoria.objects.filter(eliminado=False)

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')

        subcategoria = get_object_or_404(Subcategoria, id=categoria_id)



        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.marca = request.POST.get('marca')
        producto.categoria = subcategoria

        # Si hay una nueva imagen, actualizarla
        if request.FILES.get('imagen'):
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        
        messages.success(request, "El producto ha sido actualizado correctamente.")
        return redirect('productos_admin')

    return render(request, 'administracion/editar_producto.html', {'producto': producto,
                                                                   'subcategorias': subcategorias})

def eliminar_producto_admin(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)

    if request.method == 'POST':
        producto.eliminado = True
        producto.save()
        messages.success(request, f'El producto "{producto.nombre}" ha sido eliminado exitosamente.')
        return redirect('productos_admin')
    return redirect('productos_admin')

def categorias_admin(request):
    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'nombre')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        categorias = Categoria.objects.filter(nombre=search_query)
    else:
        categorias = Categoria.objects.all()

    # Ordenar usuarios por el parámetro recibido
    categorias = categorias.order_by(order)

    return render(request, 'administracion/categorias_admin.html', {
        'categorias':categorias,
        
        'search_query': search_query,
        'order': order,
    })

def editar_categoria_admin(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)

    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        
        categoria.save()
        
        messages.success(request, "La categoría ha sido actualizada correctamente.")
        return redirect('categorias_admin')

    return render(request, 'administracion/editar_categoria.html', {'categoria': categoria})


def eliminar_categoria_admin(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)

    if request.method == 'POST':
        categoria.eliminado = True
        categoria.save()
        messages.success(request, f'La categoría "{categoria.nombre}" ha sido eliminada exitosamente.')
        return redirect('categorias_admin')
    return redirect('categorias_admin')

def subcategorias_admin(request):
    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'nombre')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        subcategorias = Subcategoria.objects.filter(nombre=search_query)
    else:
        subcategorias = Subcategoria.objects.all()

    # Ordenar usuarios por el parámetro recibido
    subcategorias = subcategorias.order_by(order)

    return render(request, 'administracion/subcategorias_admin.html', {
        'subcategorias':subcategorias,
        
        'search_query': search_query,
        'order': order,
    })

def editar_subcategoria_admin(request, id_subcategoria):
    subcategoria = get_object_or_404(Subcategoria, id=id_subcategoria)
    categorias = Categoria.objects.filter(eliminado=False)

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')

        categoria = get_object_or_404(Categoria, id=categoria_id)
        subcategoria.nombre = request.POST.get('nombre')

        subcategoria.categoria = categoria

        subcategoria.save()
        
        messages.success(request, "La categoría ha sido actualizada correctamente.")
        return redirect('subcategorias_admin')

    return render(request, 'administracion/editar_subcategoria.html', {'subcategoria': subcategoria,
                                                                   'categorias': categorias})

def eliminar_subcategoria_admin(request, id_subcategoria):
    subcategoria = get_object_or_404(Subcategoria, id=id_subcategoria)

    if request.method == 'POST':
        subcategoria.eliminado = True
        subcategoria.save()
        messages.success(request, f'La subcategoría "{subcategoria.nombre}" ha sido eliminada exitosamente.')
        return redirect('subcategorias_admin')
    return redirect('subcategorias_admin')


def personas_admin(request):
    # Obtener el término de búsqueda y el orden
    search_query = request.GET.get('search', '').strip()
    order = request.GET.get('order', 'nombres')  # Por defecto, ordenar por 'nombre'

    # Filtrar usuarios por nombre si hay un término de búsqueda
    if search_query:
        personas = Persona.objects.filter(nombres=search_query)
    else:
        personas = Persona.objects.all()

    # Ordenar usuarios por el parámetro recibido
    personas = personas.order_by(order)

    return render(request, 'administracion/personas_admin.html', {
        'personas':personas,
        
        'search_query': search_query,
        'order': order,
    })

def editar_persona_admin(request, identificacion):
    # Obtener la persona según la identificación
    persona = get_object_or_404(Persona, identificacion=identificacion)

    if request.method == 'POST':
        # Crear el formulario con los datos enviados (POST)
        form = PersonForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            messages.success(request, "La persona ha sido actualizada correctamente.")
            return redirect('personas_admin')
    else:
        # Crear el formulario con la instancia existente
        form = PersonForm(instance=persona)

    # Pasar el formulario al contexto para renderizarlo en la plantilla
    return render(request, 'administracion/editar_persona.html', {'form': form, 'persona': persona})

    

def eliminar_persona_admin(request, identificacion):
    persona = get_object_or_404(Persona, identificacion=identificacion)

    if request.method == 'POST':
        persona.habilitado = False
        persona.eliminado = True
        persona.save()
        messages.success(request, f'La persona "{persona.nombres} {persona.apellidos}" ha sido eliminada exitosamente.')
        return redirect('personas_admin')
    return redirect('personas_admin')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def toggle_user_status(request, user_id):
    user = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'true'
        user.is_active = is_active
        user.save()

        # Mensaje de éxito
        status_text = "activado" if is_active else "desactivado"
        messages.success(request, f'El usuario "<strong>{user.username}</strong>" fue {status_text} correctamente.')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': f'El usuario "{user.username}" fue {status_text} correctamente.'})
        return redirect('usuarios_admin')

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('usuarios_admin')
    
    


@csrf_exempt
def toggle_oferente_status(request, user_id):
    user = get_object_or_404(Oferente, id=user_id)
    if request.method == 'POST':

        # Validar que el usuario no esté eliminado
        if user.eliminado:  # Asegúrate de que el campo 'eliminado' existe en el modelo
            return JsonResponse({'error': 'No se puede activar un usuario eliminado'}, status=400)


        is_active = request.POST.get('is_active') == 'true'
        user.habilitado = is_active
        user.save()

        # Mensaje de éxito
        status_text = "activado" if is_active else "desactivado"
        messages.success(request, f'El comercio "<strong>{user.nombrecomercio}</strong>" fue {status_text} correctamente.')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': f'El comercio "{user.nombrecomercio}" fue {status_text} correctamente.'})
        return redirect('usuarios_admin')

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('usuarios_admin')


@csrf_exempt
def toggle_oferta_status(request, user_id):
    user = get_object_or_404(Oferta, id=user_id)
    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'true'
        user.activo = is_active
        user.save()

        # Mensaje de éxito
        status_text = "activada" if is_active else "desactivada"
        messages.success(request, f'La oferta de "<strong>{user.titulo}</strong>" fue {status_text} correctamente.')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': f'El comercio "{user.titulo}" fue {status_text} correctamente.'})
        return redirect('ofertas_admin')

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('ofertas_admin')
    
@csrf_exempt
def toggle_persona_status(request, identificacion):
    user = get_object_or_404(Persona, identificacion=identificacion)
    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'true'
        user.habilitado = is_active
        user.save()

        # Mensaje de éxito
        status_text = "activada" if is_active else "desactivada"
        messages.success(request, f'La Persona "<strong>{user.nombres} {user.apellidos}</strong>" fue {status_text} correctamente.')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': f'La persona "{user.nombres} {user.apellidos}" fue {status_text} correctamente.'})
        return redirect('personas_admin')

    else:
        messages.error(request, 'Método no permitido.')
        return redirect('personas_admin')






#ESTADISTICAS-MICA
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from oferente.models import Oferente
from oferta.models import  Oferta
from persona.models import ubicaciones
from usuario.models import ActividadUsuario, Usuario
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractHour
from django.views.decorators.csrf import csrf_exempt



def estadisticas_con_graficos(request, categoria_id=None):
    if  request.headers.get('x-requested-with') == 'XMLHttpRequest': 
    
        if categoria_id:
            ofertas_mas_puntuadas = Oferta.objects.annotate(
                promedio_puntuacion=Avg('puntuacion__calificacion')
            ).filter(productos__categoria__categoria=categoria_id).order_by('-promedio_puntuacion')[:5]

            ofertas_mas_comentadas = Oferta.objects.annotate(
                total_comentarios=Count('comentario')
            ).filter(productos__categoria__categoria=categoria_id).order_by('-total_comentarios')[:5]

            oferentes_interaccion = Oferente.objects.annotate(
                promedio_puntuacion=Avg('ofertas__puntuacion__calificacion'),
                total_comentarios=Count('ofertas__comentario')
            ).order_by('-promedio_puntuacion', '-total_comentarios')
        else:
            ofertas_mas_puntuadas = Oferta.objects.annotate(promedio_puntuacion=Avg('puntuacion__calificacion')).order_by('-promedio_puntuacion')[:5]
            ofertas_mas_comentadas = Oferta.objects.annotate(total_comentarios=Count('comentario')).order_by('-total_comentarios')[:5]
            oferentes_interaccion = Oferente.objects.annotate(
                promedio_puntuacion=Avg('ofertas__puntuacion__calificacion'),
                total_comentarios=Count('ofertas__comentario')
            ).order_by('-promedio_puntuacion', '-total_comentarios')[:5]
        
        trafico_por_mes = list(
            ActividadUsuario.objects
            .annotate(mes=ExtractMonth('actividadinicio'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )

        # Tráfico por día
        trafico_por_dia = list(
            ActividadUsuario.objects
            .annotate(dia=ExtractDay('actividadinicio'))
            .values('dia')
            .annotate(total=Count('id'))
            .order_by('dia')
        )

        # Tráfico por hora
        trafico_por_hora = list(
            ActividadUsuario.objects
            .annotate(hora=ExtractHour('actividadinicio'))
            .values('hora')
            .annotate(total=Count('id'))
            .order_by('hora')
        )
        
        

    # Preparar datos para gráficos
    
        data = {
            
            "ofertas_mas_puntuadas": {
                "labels": [oferta.titulo for oferta in ofertas_mas_puntuadas],
                "data": [oferta.promedio_puntuacion or 0 for oferta in ofertas_mas_puntuadas],
            },
            "ofertas_mas_comentadas": {
                "labels": [oferta.titulo for oferta in ofertas_mas_comentadas],
                "data": [oferta.total_comentarios for oferta in ofertas_mas_comentadas],
            },
            "oferentes_interaccion": {
                "labels": [oferente.nombrecomercio for oferente in oferentes_interaccion],
                "data_puntuacion": [oferente.promedio_puntuacion or 0 for oferente in oferentes_interaccion],
                "data_comentarios": [oferente.total_comentarios for oferente in oferentes_interaccion],
            },
            'trafico_por_mes': trafico_por_mes,
            'trafico_por_dia': trafico_por_dia,
            'trafico_por_hora': trafico_por_hora,
            
        }
        return JsonResponse(data)  # Devuelve JSON solo en caso de AJAX

    # Renderiza HTML si no es AJAX
    return render(request, "administracion/estadistica_ofertas.html")

    
    

@csrf_exempt
def mapa_calor_inicio_sesion(request):
    if request.method == "GET":
        # Verificar si la solicitud es AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Proceso para devolver JSON
            inicios_por_ubicacion = (
                ActividadUsuario.objects
                .filter(
                    usuario__persona_id__ubicacion__latitud__isnull=False,
                    usuario__persona_id__ubicacion__longitud__isnull=False
                )
                .values('usuario__persona_id__ubicacion__latitud', 'usuario__persona_id__ubicacion__longitud')
                .annotate(total=Count('id'))
            )
            
            persona = request.user.persona_id
            ubicacion_usuario = get_object_or_404(ubicaciones, persona_id=persona)

            lat_usuario = float(ubicacion_usuario.latitud)
            lon_usuario = float(ubicacion_usuario.longitud)

            data = [
                {
                    
                    'lat': ubicacion['usuario__persona_id__ubicacion__latitud'],
                    'lng': ubicacion['usuario__persona_id__ubicacion__longitud'],
                    'count': ubicacion['total'],
                    'ubicacion_usuario': {'latitud': lat_usuario, 'longitud': lon_usuario},
                    
                }
                for ubicacion in inicios_por_ubicacion
            ]
            return JsonResponse({'data': data})

        # Si no es una solicitud AJAX, renderiza la página
        return render(request, "administracion/mapa_calor.html")

    return JsonResponse({'error': 'Método no permitido'}, status=405)


#AUDITORIAS

def auditoria_admin(request):
    return render(request, 'administracion/auditoria_admin.html')

def auditoria_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'administracion/auditoria_usuario.html', {'usuarios':usuarios})

def auditoria_personas(request):
    personas = Persona.objects.all()
    return render(request, 'administracion/auditoria_personas.html', {'personas':personas})

def auditoria_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'administracion/auditoria_ofertas.html', {'ofertas':ofertas})

def auditoria_comercios(request):
    comercios = Oferente.objects.all()
    return render(request, 'administracion/auditoria_comercios.html', {'comercios':comercios})

def auditoria_productos(request):
    productos = Producto.objects.all()
    return render(request, 'administracion/auditoria_productos.html', {'productos':productos})

def auditoria_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'administracion/auditoria_categorias.html', {'categorias':categorias})

def auditoria_subcategorias(request):
    subcategorias = Subcategoria.objects.all()
    return render(request, 'administracion/auditoria_subcategorias.html', {'subcategorias':subcategorias})

