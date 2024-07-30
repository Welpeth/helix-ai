# Bem-vindo ao HELIX AI

![Helix AI](Flask_Application/static/images/image1.png)

Uma IA criada com TensorFlow para ser usada em ambientes onde ela possa detectar padrões e responder perguntas.

## Instruções de Uso

1. **Instale o Python**: Certifique-se de ter a versão mais recente do Python instalada no seu sistema e ter o git instalado.

2. **Clone o Repositório**: No terminal do bash, navegue até o diretório onde deseja clonar o repositório e execute:

    ```bash
    git clone https://github.com/Welpeth/helix-ai
    ```

2. **Navegue até o Repositório Clonado**: No terminal do powershell de cd no helix-ai:

    ```bash
    cd helix-ai
    ```

3. **Instale as Dependências**: Instale as dependências necessárias com os seguintes comandos:

    ```bash
    pip install -r requirements.txt
    ```
    ```bash
    pip install scikit-learn gensim keras tensorflow spacy flask unidecode nltk
    ```
    ```bash
    python -m spacy download pt_core_news_lg
    ```

4. **Execute o Treinamento**: Com as dependências instaladas, você pode **abrir o terminal do powershell** ir até o diretorio onde a pasta principal do Helix AI está, e execute:

    ```bash
    python model_training.py
    ```

5. **Execute o Aplicativo**: Com as dependências instaladas, e o Helix AI pronto, vá para a pasta Flask_Application pelo powershell e execute:

    ```bash
    python app.py
    ```

6. **Abra no navegador**: Com tudo pronto e o app.py funcionando perfeitamente abra no localhost:

    ```
    127.0.0.1:5000
    ```

Agora você pode usar o Helix AI para detectar padrões e responder perguntas.
