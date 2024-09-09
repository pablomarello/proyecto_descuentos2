import requests
from xml.etree import ElementTree as ET
from cryptography import *

from OpenSSL import crypto
import time
from datetime import datetime, timedelta

# Cargar la clave privada y el certificado
private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open('private_key.pem').read())
cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('certificadosll.pem').read())

# Crear el ticket de requerimiento (TRA)
tra = ET.Element('loginTicketRequest')
header = ET.SubElement(tra, 'header')
unique_id = ET.SubElement(header, 'uniqueId').text = str(int(time.time()))
generation_time = ET.SubElement(header, 'generationTime').text = (datetime.now() - timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S')
expiration_time = ET.SubElement(header, 'expirationTime').text = (datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S')
service = ET.SubElement(tra, 'service').text = 'ws_sr_padron_a13'

tra_str = ET.tostring(tra).decode('utf-8')
tra_signed = crypto.sign(private_key, tra_str, 'sha256')

# Hacer la petición al WSAA
url = 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl'
response = requests.post(url, data=tra_signed, headers={'Content-Type': 'application/octet-stream'})

# Parsear la respuesta para obtener Token y Sign
root = ET.fromstring(response.content)
token = root.find('.//token').text
sign = root.find('.//sign').text

print(f"Token: {token}")
print(f"Sign: {sign}")
