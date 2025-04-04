# Chatbot Interativo City

Bem-vindo ao projeto Chatbot Interativo City! Este repositório contém um chatbot simples desenvolvido em Python, utilizando Flask para o backend e uma interface web estática para interação com o usuário.


## Visão Geral

Este projeto implementa um chatbot básico que responde a perguntas predefinidas. Ele utiliza o Flask para criar um servidor web que serve uma página HTML estática, permitindo que os usuários interajam com o chatbot através de uma interface web.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados em sua máquina:

- Python 3.x

- Git

## Instalação

Siga os passos abaixo para configurar e executar o projeto em sua máquina local:

## Clone o repositório
```bash
git clone https://github.com/Emanuel-nx/chatbot_interativo_city.git
```
## Navegue até o diretório do projeto
```bash
cd chatbot_interativo_city
```
## Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
```
## Ative o ambiente virtual
### No Windows:
```bash
venv\Scripts\activate
```
### No macOS/Linux:
```bash
source venv/bin/activate
```
## Instale as dependências
```bash
pip install -r requirements.txt
```
# Estrutura do Projeto

A estrutura básica do projeto é a seguinte:

```bash
chatbot_interativo_city/
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── app.py
├── main.py
├── requirements.txt
└── .gitignore
```
## Explicação dos Blocos de Código
```bash
app.py
```
```bash
from flask import Flask, render_template, request
from main import get_bot_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    return str(get_bot_response(user_text))

if __name__ == "__main__":
    app.run()
```

## Cria o servidor Flask e define as rotas para servir a interface web e processar mensagens do chatbot.
```bash
main.py
```
```bash
def get_bot_response(user_input):
    responses = {
        "oi": "Olá! Como posso ajudar você hoje?",
        "qual é o seu nome?": "Eu sou um chatbot criado para ajudar você.",
        "adeus": "Tchau! Tenha um ótimo dia!"
    }
    return responses.get(user_input.lower(), "Desculpe, não entendi sua pergunta.")
```

Define respostas predefinidas para mensagens específicas do usuário.

## Glossário

- Flask: Um micro framework web em Python para desenvolver aplicações web.

- Render Template: Função do Flask que renderiza arquivos HTML e os retorna como resposta.

- Rota: URL associada a uma função específica no backend.

- Ambiente Virtual: Espaço isolado para gerenciar dependências do projeto.

## Como Testar a Aplicação

Execute o seguinte comando para iniciar o servidor:
```bash
python app.py
```
## A saída será semelhante a esta:
```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Abra seu navegador e acesse:

```bash http://localhost:5000/static/index.html ```

# Você verá a interface do chatbot pronta para interação.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias e correções.
