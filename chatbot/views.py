import os
from django.shortcuts import render
from django.http import JsonResponse
import random
import json
import pickle
import numpy as np
import nltk
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from nltk.stem import WordNetLemmatizer
from keras.models import load_model



# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar los recursos del chatbot usando rutas absolutas
lemmatizer = WordNetLemmatizer()
intents_path = os.path.join(current_dir, 'datos_chatbot/intents.json')
words_path = os.path.join(current_dir, 'datos_chatbot/words.pkl')
classes_path = os.path.join(current_dir, 'datos_chatbot/classes.pkl')
model_path = os.path.join(current_dir, 'datos_chatbot/chatbot_model.h5')

# Cargar los archivos
intents = json.loads(open(intents_path, encoding='utf-8').read())
words = pickle.load(open(words_path, 'rb'))
classes = pickle.load(open(classes_path, 'rb'))
model = load_model(model_path)


# Funciones del chatbot para preprocesamiento, predicción y respuesta
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, threshold=0.3):  # Agregar el parámetro threshold
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.argmax(res)
    confidence = res[max_index]  # Obtener la confianza de la predicción

    if confidence >= threshold:
        category = classes[max_index]
    else:
        category = None  # Indicar que no se tiene suficiente confianza en la predicción

    return category

def get_response(tag, intents_json):
    if tag is None:
        return "Lo siento, no entendí tu pregunta."  # Respuesta para baja confianza

    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i["tag"] == tag:
            return random.choice(i['responses'])
    return "Lo siento, no entendí tu pregunta."

# Vista para procesar los mensajes de los usuarios
def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        tag = predict_class(user_input)
        bot_response = get_response(tag, intents)
        return JsonResponse({'response': bot_response})
    
    return render(request, 'chatbot/chatbot.html')