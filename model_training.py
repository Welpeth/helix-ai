import random
import json
import pickle
import numpy as np
import nltk
nltk.download('rslp')
nltk.download('punkt')
import sklearn
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

# Initialize the stemmer
stemmer = RSLPStemmer()

# Load intents
with open('model/intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Function to normalize slang and synonyms
def normalize_text(text):
    slang_dict = {
        'config': 'configurações',
        'net': 'internet',
        'oq' : 'o que',
        'adpt': 'adaptador',
        'pst': 'pasta',
        'vc': 'você',
        'tb': 'também',
        'pq': 'porque',
        'bff': 'melhor amigo para sempre',
        'q': 'que',
        'dps': 'depois',
        'blz': 'beleza',
        'tmj': 'tamo junto',
        'p': 'para',
        'td': 'tudo',
        'qdo': 'quando',
        'nd': 'nada',
        'lol': 'rir alto',
        'tbm': 'também',
        'hj': 'hoje',
        'am': 'amigo',
        'tô': 'estou',
        'msg': 'mensagem',
        'n': 'não',
        'sim': 'sim',
        'vlw': 'valeu',
        'grd': 'grande',
        'wpp': 'whatsapp',
        'pode crer': 'pode acreditar',
        'bjs': 'beijos',
        'abs': 'abraços',
        'emo': 'emocional',
        'kkk': 'risada',
        'aff': 'aflito/irritado',
        'lkk': 'risada',
        'flw': 'falou',
        'vlw': 'valeu'
    }
    words = text.split()
    normalized_words = [slang_dict.get(word, word) for word in words]
    return ' '.join(normalized_words)

# Process intents
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

def load_keywords():
    with open('model/keywords.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [{'keywords': entry['keywords'], 'responses': entry['responses']} for entry in data['keywords']]

for intent in intents['intents']:
    for pattern in intent['patterns']:
        normalized_pattern = normalize_text(pattern)
        word_list = word_tokenize(normalized_pattern, language='portuguese')
        words.extend(word_list)
        keywords = load_keywords()
        documents.append((word_list, intent['tag']))

        for keyword in keywords:
            for key in keyword['keywords']:
                if key not in word_list:
                    word_list.append(key)

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Apply stemming
words = [stemmer.stem(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Save words and classes
pickle.dump(words, open('model/words.pkl', 'wb'))
pickle.dump(classes, open('model/classes.pkl', 'wb'))

# Prepare data for training
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

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(train_x, train_y, test_size=0.2, random_state=42)

# Build and train the model
model = Sequential()
model.add(Dense(1024, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=1200, batch_size=5, validation_data=(X_val, y_val), verbose=1)

# Save the trained model
model.save('model/chatbot_model.keras')