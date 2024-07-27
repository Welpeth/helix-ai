import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Inicializar o stemmer
stemmer = RSLPStemmer()

# Carregar intents
with open('model/intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Processar intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = word_tokenize(pattern, language='portuguese')
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Aplicar stemming
words = [stemmer.stem(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

# Salvar palavras e classes
pickle.dump(words, open('model/words.pkl', 'wb'))
pickle.dump(classes, open('model/classes.pkl', 'wb'))

# Preparar dados para treinamento
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [stemmer.stem(word.lower()) for word in word_patterns]

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append((np.array(bag), np.array(output_row)))

random.shuffle(training)

train_x = np.array([t[0] for t in training])
train_y = np.array([t[1] for t in training])

# Construir e treinar o modelo
model = Sequential()
model.add(Dense(512, input_shape=(len(train_x[0]),), activation='relu'))  # Aumentado para 512 neurônios
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))  # Aumentado para 256 neurônios
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))  # Aumentado para 128 neurônios
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))   # Adicionada nova camada com 64 neurônios
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Atualizar para usar o novo formato do SGD
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=5, verbose=1)

# Salvar o modelo treinado
model.save('model/chatbot_model.keras')
