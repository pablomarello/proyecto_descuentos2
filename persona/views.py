from django.shortcuts import get_object_or_404, render, redirect

from persona.models import Persona, TablaMunicipio, TablaProvincia, ubicaciones,TablaDepartamento,TablaLocalidad
from persona.forms import FormPersona, Formubi
from django.contrib import messages
from django.http import JsonResponse
import requests
from django.conf import settings


# Create your views here.



def registrar_persona(request):
    if request.method == 'POST':
        form = FormPersona(request.POST)
        if form.is_valid():
            persona = form.save()
                # Guarda la instancia de Persona creada con los datos del formulario
             # Redirige al formulario de registro de usuario pasando el ID de la persona creada como parámetro
            print(persona.pk)
            return redirect('registrar_ubicacion', persona_id=persona.pk)#, persona_id=persona.pk
        else: messages.error(request, 'Verifique los datos registrados')
    else:
        form = FormPersona()
    return render(request, 'personas/registro_personas.html', {'form': form})


def load_provincias(request):
    pais_id = request.GET.get('cod_pais') 
    if pais_id:
        provincias = TablaProvincia.objects.filter(pais_id_id=pais_id).order_by('nom_pcia')
        data = list(provincias.values('cod_pcia', 'nom_pcia'))
    else:
        data = []
    return JsonResponse(data, safe=False)

def load_deptos(request):
    provincia_id = request.GET.get('cod_pcia')  
    if provincia_id:
        departamentos = TablaDepartamento.objects.filter(provincia_id_id=provincia_id).order_by('nom_depto')
        data = list(departamentos.values('cod_depto', 'nom_depto'))
    else:
        data = []
    return JsonResponse(data, safe=False)

def load_municipios(request):
    depto_id = request.GET.get('depto_id')  
    if depto_id:
        municipios = TablaMunicipio.objects.filter(departamento_id_id=depto_id).order_by('nom_agl')
        data = list(municipios.values('cod_agl', 'nom_agl'))
    else:
        data = []
    return JsonResponse(data, safe=False)


def load_localidad(request):
    municipio_id = request.GET.get('municipio_id')  
    if municipio_id:
        localidades = TablaLocalidad.objects.filter(municipio_id_id=municipio_id).order_by('nombre')
        data = list(localidades.values('cod_ase', 'nombre'))
    else:
        data = []
    return JsonResponse(data, safe=False)





def mostrar_mapa(request):
    ubicacion = ubicaciones.objects.all()  # Obtener todas las ubicaciones
    coordenadas = [
        {
            'latitud': float(u.latitud) if u.latitud is not None else None,
            'longitud': float(u.longitud) if u.longitud is not None else None
        }
        for u in ubicacion
        ]    
    return render(request, 'personas/mostrar_ubicacion.html', {'coordenadas': coordenadas})



def registrar_ubicacion(request,persona_id):
    persona = get_object_or_404(Persona, pk=persona_id)
    if request.method=='POST':
        form=Formubi(request.POST)
        if form.is_valid():
            ubicacion= form.save(commit=False)
            ubicacion.persona_id=persona
            ubicacion.save()
            return redirect('registrar_usuario',persona_id=persona.pk)
        else: messages.error(request, 'Verifique los datos registrados')
    else:
        form = Formubi()
    return render(request, 'personas/registrar_ubicacion.html', {'form': form})

