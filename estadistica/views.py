from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from oferente.models import Oferente
from oferta.models import Comentario, Oferta, Puntuacion
from persona.models import ubicaciones
from producto.models import Producto, Subcategoria
from usuario.models import ActividadUsuario, Usuario
from django.db.models import Avg, Count, F, Q
import json
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractHour
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncDay
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
    return render(request, "admin/estadistica_ofertas.html")

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Asegura que solo usuarios autenticados puedan acceder
def estadisticas_oferente(request, categoria_id=None):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        oferentes = request.user.comercios.all()
        filtros = {'oferente__in': oferentes}
        
        if categoria_id:
            filtros['productos__categoria__id'] = categoria_id

        # Filtrar ofertas relevantes
        
        ofertas_mas_puntuadas = Oferta.objects.filter(**filtros).annotate(
            promedio_puntuacion=Avg('puntuacion__calificacion')
        )

        ofertas_mas_comentadas = Oferta.objects.filter(**filtros).annotate(
            total_comentarios=Count('comentario')
        )
        
        ofertas= Oferta.objects.filter(**filtros)

        estadisticas_por_comercio = [
            
            {
                "comercio": oferente.nombrecomercio,
                "total_ofertas": ofertas.filter(oferente=oferente).count(),
                "ofertas_mayor_4": ofertas_mas_puntuadas.filter(oferente=oferente, promedio_puntuacion__gt=3.9).count(),
                "ofertas_menor_4":ofertas_mas_puntuadas.filter(oferente=oferente, promedio_puntuacion__lte=3.9).count(),
                "mas_comentadas": list(
                    ofertas_mas_comentadas.filter(oferente=oferente).values('id', 'titulo', 'total_comentarios','activo')
                ),
                "mejor_puntuadas": list(
                    ofertas_mas_puntuadas.filter(oferente=oferente).values('id', 'titulo', 'promedio_puntuacion','activo')
                ),
                
            }
            for oferente in oferentes
        ]

        return JsonResponse({'estadisticas_por_comercio': estadisticas_por_comercio})
    else:
        return render(request, 'oferente/estadisticas.html')
    
    

@csrf_exempt
def mapa_calor_inicio_sesion(request, categoria_id=None):
    if request.method == "GET":
        # Verificar si la solicitud es AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Proceso para devolver JSON
                # Obtener ofertas más puntuadas
                if categoria_id:
                    ofertas_mas_puntuadas = Oferta.objects.annotate(
                        promedio_puntuacion=Avg('puntuacion__calificacion')
                    ).filter(productos__categoria__categoria=categoria_id).order_by('-promedio_puntuacion')[:5]
                else:
                    ofertas_mas_puntuadas = Oferta.objects.annotate(
                        promedio_puntuacion=Avg('puntuacion__calificacion')
                    ).order_by('-promedio_puntuacion')[:5]

                # Validar ofertas
                ofertas_data = [
                    {
                        'id': oferta.id,
                        'nombre': oferta.titulo,
                        'promedio_puntuacion': oferta.promedio_puntuacion,
                        'lat': oferta.comercio.ubicacion.latitud if oferta.comercio and oferta.comercio.ubicacion else None,
                        'lng': oferta.comercio.ubicacion.longitud if oferta.comercio and oferta.comercio.ubicacion else None
                    }
                    for oferta in ofertas_mas_puntuadas
                ]

                # Obtener inicios por ubicación
                inicios_por_ubicacion = (
                    ActividadUsuario.objects
                    .filter(
                        usuario__persona_id__ubicacion__latitud__isnull=False,
                        usuario__persona_id__ubicacion__longitud__isnull=False
                    )
                    .values('usuario__persona_id__ubicacion__latitud', 'usuario__persona_id__ubicacion__longitud')
                    .annotate(total=Count('id'))
                )

                # Ubicación del usuario
                try:
                    persona = request.user.persona_id
                    ubicacion_usuario = get_object_or_404(ubicaciones, persona_id=persona)
                    lat_usuario = float(ubicacion_usuario.latitud)
                    lon_usuario = float(ubicacion_usuario.longitud)
                except Exception as e:
                    lat_usuario, lon_usuario = None, None
                    print(f"Error obteniendo la ubicación del usuario: {e}")

                # Preparar datos para JSON
                data = {
                    'ubicaciones_inicios': [
                        {
                            'lat': ubicacion['usuario__persona_id__ubicacion__latitud'],
                            'lng': ubicacion['usuario__persona_id__ubicacion__longitud'],
                            'count': ubicacion['total']
                        }
                        for ubicacion in inicios_por_ubicacion
                    ],
                    'ubicacion_usuario': {'latitud': lat_usuario, 'longitud': lon_usuario},
                    'ofertas_mas_puntuadas': ofertas_data
                }
                return JsonResponse(data)

        # Si no es una solicitud AJAX, renderiza la página
        return render(request, "admin/mapa_calor.html")

    return JsonResponse({'error': 'Método no permitido'}, status=405)


