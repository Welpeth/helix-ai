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

    intents_list = predict_class(message)
    response = get_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
