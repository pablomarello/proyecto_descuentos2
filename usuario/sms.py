from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from urllib.parse import urlencode

@csrf_exempt
def send_sms(numero, texto):
    apikey = "h0lbgsj2yccm4fc72ys6elim6wcduo7c86090jffabfigts5e1th0ppmv1ispzwr6fwne4ja40sio1df7b4l8vq4e18af9edacyc"

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