from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.parse import urlencode
from proyecto_descuentos2.settings import Apy_telefono

@csrf_exempt
def send_sms(numero, texto):
    apikey = Apy_telefono

    # Construye la URL
    base_url = "http://servicio.smsmasivos.com.ar/enviar_sms.asp"
    params = {
        "api": 1,
        "apikey": apikey,
        "tos": numero,
        "texto": texto
    }

    url = base_url + "?" + urlencode(params)

    # Envía la solicitud GET
    response = requests.get(url)

    # Maneja la respuesta
    if response.status_code == 200:
        response_text = response.text
    elif response.status_code == 408:
        response_text = "ERROR: Tiempo de espera agotado"
    else:
        response_text = f"ERROR: Código de estado {response.status_code}"

    return response_text