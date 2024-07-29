from flask import Flask, request, jsonify, render_template
import os

from utils import get_response, predict_class

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/documentacao')
def documentacao():
    return render_template('documentacao.html')

@app.route('/handle_message', methods=['POST'])
def handle_message():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'response': "Desculpe, não entendi sua mensagem."})

    response = get_response(message)
    return jsonify({'response': response})

@app.route('/update_intents', methods=['POST'])
def update_intents():
    data = request.json
    if 'tag' not in data or 'patterns' not in data:
        return jsonify({"error": "As chaves 'tag' e 'patterns' são obrigatórias."}), 400

    tag = data['tag']
    new_patterns = data['patterns']
    result = update_intents_file('model/intents.json', tag, new_patterns)

    return jsonify({'message': result})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if 'message' not in data:
        return jsonify({"error": "A chave 'message' é obrigatória."}), 400

    message = data['message']
    intents = predict_class(message)
    response = get_response(message)
    
    return jsonify({
        'intents': intents,
        'response': response
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)