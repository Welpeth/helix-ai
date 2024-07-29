# Bem-vindo ao HELIX AI

![Helix AI](Flask_Application/static/images/image1.png)

Uma IA criada com TensorFlow para ser usada em ambientes onde ela possa detectar padrões e responder perguntas.

## Instruções de Uso

1. **Instale o Python**: Certifique-se de ter a versão mais recente do Python instalada no seu sistema.

2. **Clone o Repositório**: No terminal do bash, navegue até o diretório onde deseja clonar o repositório e execute:

    ```bash
    git clone https://github.com/Welpeth/helix-ai
    ```

3. **Instale as Dependências**: Navegue para o diretório do projeto e instale as dependências necessárias com os seguintes comando:

    ```bash
    pip install -r requirements.txt
    pip install scikit-learn gensim keras tensorflow spacy flask unidecode nltk
    python -m spacy download pt_core_news_lg
    ```

4. **Execute o Aplicativo**: Com as dependências instaladas, você pode iniciar o Helix AI executando:

    ```bash
    python app.py
    ```

Agora você pode usar o Helix AI para detectar padrões e responder perguntas.
