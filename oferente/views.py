from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CuitForm, OferenteForm
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
            oferente.save()
            messages.success(request, "El comercio ha sido registrado exitosamente.")
            return redirect('login_user')
        else:
            messages.error(request, "Verifique los datos ingresados.")
    else:
        form = OferenteForm()
    
    return render(request, 'oferente/registrarComercio.html', {'form': form})
