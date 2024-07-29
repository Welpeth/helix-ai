from flask import Flask, request, jsonify
import numpy as np
import json
import pickle
import spacy
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from tensorflow.keras.models import load_model
import random
from unidecode import unidecode
import os

# Carregar o modelo spaCy e o modelo Keras
nlp = spacy.load('pt_core_news_lg')
model = load_model('model/chatbot_model.keras')
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))

ignore_letters = ['?', '!', '.', ',']
stemmer = RSLPStemmer()

def clean_up_sentence(sentence):
    sentence = unidecode(sentence)
    sentence = sentence.lower()
    sentence_words = word_tokenize(sentence, language='portuguese')
    sentence_words = [stemmer.stem(word) for word in sentence_words if word not in ignore_letters]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.5

    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        return [{'intent': 'not_understood', 'probability': '0.0'}]

    return_list = [{'intent': classes[r[0]], 'probability': str(r[1])} for r in results]
    return return_list

intents_json = json.load(open('model/intents.json', 'r', encoding='utf-8'))

def load_keywords():
    with open('model/keywords.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Retorna uma lista de dicionários onde cada dicionário contém um conjunto de palavras-chave e respostas
    keywords = [{'keywords': entry['keywords'], 'responses': entry['responses']} for entry in data['keywords']]
    return keywords

def check_keywords(text):
    keywords = load_keywords()
    text = text.lower()
    for entry in keywords:
        if any(keyword in text for keyword in entry['keywords']):
            return random.choice(entry['responses'])  # Escolhe uma resposta aleatória da lista de respostas
    return None


def get_response(message):
    # Verificar palavras-chave
    keyword_response = check_keywords(message)
    if keyword_response:
        return keyword_response
    
    if not isinstance(message, str):
        raise ValueError("A entrada deve ser uma string.")
    
    message_doc = nlp(message.lower())
    
    highest_similarity = 0
    best_tag = 'not_understood'
    
    for intent in intents_json['intents']:
        for pattern in intent['patterns']:
            pattern_doc = nlp(pattern.lower())
            similarity = message_doc.similarity(pattern_doc)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_tag = intent['tag']
    
    MIN_SIMILARITY_THRESHOLD = 0.5
    if highest_similarity < MIN_SIMILARITY_THRESHOLD:
        return "Desculpe, não consegui encontrar uma resposta para sua pergunta."
    
    for intent in intents_json['intents']:
        if intent['tag'] == best_tag:
            responses = intent.get('responses', [])
            if responses:
                return random.choice(responses)
    
    return "Desculpe, não consegui encontrar uma resposta para sua pergunta."