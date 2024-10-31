from django.shortcuts import render
from django.http import JsonResponse
import random
import nltk
from nltk.chat.util import Chat, reflections

# Definimos algunos patrones y respuestas
pairs = [
    (r'(?i)(hola|hol+a+|buenos dias|buenas|saludos)', ['¡Hola! Bienvenido a Descuentos Catamarca. ¿Cómo puedo ayudarte?']),
    (r'(?i)(ofertas|promociones|descuentos)', ['Tenemos varias ofertas. Puedes filtrarlas por categoría, precio y producto en nuestro sitio.']),
    (r'(?i)(hasta cuando estan las ofertas|duracion ofertas|vigencia de las ofertas)', ['Las ofertas están disponibles hasta la fecha indicado en cada oferta.']),
    (r'(?i)(como puedo registrarme|registrarme|crear cuenta)', ['Para registrarte, haz clic en <a href="/persona/registrar" style="color: blue;">Registrarse</a> y sigue los pasos.']),
    (r'(?i)(como cargar comercio|subir comercio|registrar comercio)', ['Para registrar tu comercio hacé clic <a href="/oferente/verificar_cuit" style="color: blue;">AQUÍ']),
    (r'(?i)(puedo cargar mas de un comercio|varios comercios)', ['Sí, puedes cargar más de un comercio por usuario.']),
    (r'(?i)(como cargar productos|cargar producto|subir producto)', ['Si no encuentras un producto para cargarlo en la oferta en nuestro sitio, puedes agregarlo tú mismo.']),
    (r'(?i)(ubicacion del comercio|donde esta el comercio)', ['Puedes ver la ubicación del comercio en el detalle de la oferta, e incluso trazar una ruta desde tu ubicación.']),
    (r'(?i)(puedo comentar o valorar las ofertas|comentar o valorar ofertas|como comento y valoro las ofertas|valorar y comentar ofertas)', ['Sí, puedes comentar y valorar ofertas si estás registrado.']),
    (r'(?i)(puedo valorar las ofertas)', ['Si,puedes valorar las ofertas pero solamente si estás registrado.']),
    (r'(?i)(como valoro las ofertas|como valorar ofertas|valorar ofertas)', ['Para valorar las ofertas debes entrar en el detalle de la oferta y te aparecera unas estrellas que te permiten darle la calificacion a la oferta solamente tienes que hacer click para calificar esto solamente funciona si estas registrado.']),
    (r'(?i)(puedo comentar las ofertas)', ['Si,puedes comentar las ofertas pero solamente si estás registrado.']),
    (r'(?i)(como comento las ofertas|como comentar ofertas|comentar ofertas)', ['Para comentar las ofertas debes entrar en el detalle de la oferta y en el apartado de compentarios se te permitira comentar si estas registrado.']),
    (r'(?i)(que te permite hacer la lista de compras|que permite la lista de compras)', ['La lista de compras te permite guardar ofertas y trazar una ruta entre los comercios desde tu ubicación.']),
    (r'(?i)(como usar lista de compras|como se usa la lista de compras|como utilizo la lista de compras|como utilizar la lista de compras|utilizar lista compras)', ['Para utilizar la lista de compras primero debes estar registrado, una vez, registrado cuando estres al detalle de una oferta te aparecera el boton agregar a la lista de compras ahi se guardaran las ofertas que seleccionaste y te permitira trazar la ruta adonde se encuentra los comercios con las ofertas deseadas.']),
    (r'(?i)(como funciona el chatbot|ayuda)', ['Estoy aquí para responder tus preguntas sobre Descuentos Catamarca. Pregúntame sobre ofertas, registro, comercios y más.']),
    (r'(.*)', ['Lo siento, no entendí tu pregunta. Puedes preguntarme sobre las ofertas, registro de comercios, o cómo usar la lista de compras en Descuentos Catamarca.'])
]

# Inicializamos el chatbot
chatbot = Chat(pairs, reflections)

def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        bot_response = chatbot.respond(user_input)
        return JsonResponse({'response': bot_response})

    return render(request, 'chatbot/chatbot.html')    
