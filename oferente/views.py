from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from persona.models import TablaDepartamento, TablaLocalidad, TablaMunicipio, TablaProvincia
from .forms import CuitForm, OferenteForm, UbiComercio
from .models import Oferente
from afip import Afip

cert = open('oferente/certificado.crt').read()
key = open('oferente/private_key.key').read()

afip = Afip({
    "CUIT": 23395413929,
    "cert": cert,
    "key": key,
    "access_token": "nAHMdh4PFKr4JXcyNy751LloC7UUCdlS8AGpXaUNmUGzhrWVbP37zwZAN4RnbxVt",
    "production": True
})

def verificarCuit(request):
    if request.method == 'POST':
        form = CuitForm(request.POST)
        if form.is_valid():
            cuit = form.cleaned_data['cuit']
            try:
                # Verificar si el CUIT está inscrito en el padrón de AFIP
                res = afip.RegisterInscriptionProof.getTaxpayerDetails(cuit)
                print(res)
                datos_generales = res.get('datosGenerales', {})
                error_constancia = res.get('errorConstancia', {})
                
                if datos_generales:             
                    nombre = datos_generales.get('nombre', '-----')
                    apellido = datos_generales.get('apellido', '-----')
                    
                    domicilio_fiscal = datos_generales.get('domicilioFiscal', {})
                    direccion = domicilio_fiscal.get('direccion', '----')
                    
                    messages.success(request, f"ESTÁS INSCRIPTO EN AFIP. El CUIT {cuit} pertenece a {nombre} {apellido} con dirección {direccion}. Puedes continuar")
                    request.session['cuit_validado'] = cuit
                    return redirect('registrar_comercio')
                
                elif error_constancia:
                    nombre = error_constancia.get('nombre', '-----')
                    apellido = error_constancia.get('apellido', '-----')
                    
                    domicilio_fiscal = error_constancia.get('domicilioFiscal', {})
                    direccion = error_constancia.get('direccion', '----')
                    
                    messages.success(request, f"ESTÁS INSCRIPTO EN AFIP. El CUIT {cuit} pertenece a {nombre} {apellido} con dirección {direccion}. Puedes continuar")
                    request.session['cuit_validado'] = cuit
                    return redirect('registrar_comercio')
                
            except Exception as e:
                messages.error(request, f"No se encontró el CUIT ingresado: {cuit}. Error")
        else:
            messages.error(request, "Formulario no válido")
    else:
        form = CuitForm()
    
    return render(request, 'oferente/verificarCuit.html', {'form': form})

def registrarComercio(request):
    if request.method == 'POST':
        cuit = request.session.get('cuit_validado')
        form = OferenteForm(request.POST)
        if form.is_valid():
            oferente = form.save(commit=False)
            oferente.cuit = cuit
            oferente.id_usuario=request.user
            oferente.save()
            messages.success(request, "El comercio ha sido registrado exitosamente.")
            return redirect('ubicacion_comercio',oferente.pk)
        else:
            messages.error(request, "Verifique los datos ingresados.")
    else:
        form = OferenteForm()
    
    return render(request, 'oferente/registrarComercio.html', {'form': form})


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

def ubicacion_comercio(request,comercio_id):
    comercio=get_object_or_404(Oferente,pk=comercio_id)
    if request.method=='POST':
        form=UbiComercio(request.POST)
        if form.is_valid():
            ubicacion= form.save(commit=False)
            ubicacion.comercio_id=comercio
            ubicacion.save()
            return redirect('index')
        else: messages.error(request, 'Verifique los datos registrados')
    else:
        form = UbiComercio()
    return render(request, 'oferente/ubicaciones_comercio.html', {'form': form})