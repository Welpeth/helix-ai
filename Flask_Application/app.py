from flask import Flask, request, jsonify, render_template
import os
import webbrowser
from threading import Timer

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
def update_intents_file():
    data = request.get_json()
    file_path = data.get('file_path')
    tag = data.get('tag')
    new_patterns = data.get('patterns')

    if not file_path or not tag or not new_patterns:
        return jsonify({'error': 'Parâmetros insuficientes.'}), 400

    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            intent_found = False
            for intent in data['intents']:
                if intent['tag'] == tag:
                    intent['patterns'] = new_patterns
                    intent_found = True
                    break
            if not intent_found:
                data['intents'].append({'tag': tag, 'patterns': new_patterns, 'responses': []})
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.truncate()
        return jsonify({'message': 'Intents atualizados com sucesso.'})
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo não encontrado.'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Erro ao decodificar o arquivo JSON.'}), 400

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
    
    url = f'http://127.0.0.1:{port}/'
    
    def run_app():
        app.run(host='0.0.0.0', debug=True, port=port)
    
    # Função para abrir o navegador
    def open_browser():
        if not webbrowser._tryorder:
            webbrowser.open(url)
    
    Timer(1, open_browser).start()
    run_app()
