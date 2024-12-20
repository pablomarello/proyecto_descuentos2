import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

# Rutas de los archivos
intents_path = 'intents.json'
words_path = 'words.pkl'
classes_path = 'classes.pkl'

# Inicializar documentos, palabras y clases
documents = []
words = []
classes = []

# Cargar el JSON y procesar los patrones
with open(intents_path, encoding='utf-8') as file:
    intents = json.load(file)

ignore_letters = ['?', '!', '¿', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Comprobar si necesitamos actualizar words y classes
need_update = (
    not os.path.exists(words_path) or
    not os.path.exists(classes_path) or
    os.path.getmtime(intents_path) > os.path.getmtime(words_path) or
    os.path.getmtime(intents_path) > os.path.getmtime(classes_path)
)

if need_update:
    print("Actualizando palabras y clases...")
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))

    # Guardar palabras y clases
    with open(words_path, 'wb') as f:
        pickle.dump(words, f)
    with open(classes_path, 'wb') as f:
        pickle.dump(classes, f)
else:
    print("Cargando palabras y clases desde archivos pickle...")
    with open(words_path, 'rb') as f:
        words = pickle.load(f)
    with open(classes_path, 'rb') as f:
        classes = pickle.load(f)

# Verificar que documents tenga datos
if not documents:
    raise ValueError("No hay datos en documents. Verifica el archivo intents.json.")

# Vectorización de los datos para entrenamiento
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)  # Bag of words binario

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([np.array(bag), output_row])

random.shuffle(training)

# Preparación de datos de entrenamiento
train_x = []
train_y = []
for i in training:
    train_x.append(i[0].flatten())
    train_y.append(i[1])

train_x = np.array(train_x)
train_y = np.array(train_y)

# Verificar que train_x y train_y tengan datos
if train_x.size == 0 or train_y.size == 0:
    raise ValueError("train_x o train_y están vacíos. Revisa el procesamiento de datos.")

# Creación del modelo de red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(train_x.shape[1],), kernel_regularizer=l2(0.001), activation='relu', name="input_layer1"))
model.add(Dropout(0.5))
model.add(Dense(64, kernel_regularizer=l2(0.001), activation='relu', name="hidden_layer"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax', name="output_layer"))

# Compilación del modelo
sgd = SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrenamiento y guardado del modelo

history = model.fit(train_x, train_y, epochs=600, batch_size=10, verbose=1)
model.save("chatbot_model.h5")

# Graficar precisión y pérdida
plt.figure(figsize=(12, 5))

# Gráfica de la pérdida (loss)
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Pérdida de entrenamiento')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Épocas')
plt.ylabel('Pérdida')
plt.legend()

# Gráfica de la precisión (accuracy)
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Precisión de entrenamiento')
plt.title('Precisión durante el entrenamiento')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.legend()

plt.show()
