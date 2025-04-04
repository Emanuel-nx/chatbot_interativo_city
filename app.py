# Importação das bibliotecas necessárias
import os
from flask import Flask, request, jsonify  # Adicionando Flask para API
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

# Inicializar Flask
app = Flask(__name__)

# Carregar variáveis de ambiente
load_dotenv(find_dotenv())
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializar o modelo AI
model = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key=groq_api_key
)

# Dados das cidades
city_data = {
    "São Paulo": {
        "população": "12,33 milhões",
        "pontos_turisticos": ["Parque Ibirapuera", "Avenida Paulista", "Mercado Municipal", "Catedral da Sé"],
        "universidade": "Universidade de São Paulo (USP)"
    },
    "Rio de Janeiro": {
        "população": "6,7 milhões",
        "pontos_turisticos": ["Cristo Redentor", "Pão de Açúcar", "Praia de Copacabana"],
        "universidade": "Universidade Federal do Rio de Janeiro (UFRJ)"
    },
    "Salvador": {
        "população": "2,9 milhões",
        "pontos_turisticos": ["Pelourinho", "Elevador Lacerda", "Farol da Barra"],
        "universidade": "Universidade Federal da Bahia (UFBA)"
    },
    "Belo Horizonte": {
        "população": "2,5 milhões",
        "pontos_turisticos": ["Praça da Liberdade", "Igreja São José", "Museu de Artes e Ofícios"],
        "universidade": "Universidade Federal de Minas Gerais (UFMG)"
    },
    "Fortaleza": {
        "população": "2,7 milhões",
        "pontos_turisticos": ["Praia do Futuro", "Catedral Metropolitana", "Mercado Central"],
        "universidade": "Universidade Federal do Ceará (UFC)"
    },
    "Brasília": {
        "população": "3,1 milhões",
        "pontos_turisticos": ["Congresso Nacional", "Catedral de Brasília", "Palácio do Planalto"],
        "universidade": "Universidade de Brasília (UnB)"
    },
    "Curitiba": {
        "população": "1,9 milhões",
        "pontos_turisticos": ["Jardim Botânico", "Ópera de Arame", "Rua XV de Novembro"],
        "universidade": "Universidade Federal do Paraná (UFPR)"
    },
    "Porto Alegre": {
        "população": "1,5 milhões",
        "pontos_turisticos": ["Parque Redenção", "Caminho dos Antiquários", "Fundação Ibere Camargo"],
        "universidade": "Universidade Federal do Rio Grande do Sul (UFRGS)"
    },
    "Recife": {
        "população": "1,6 milhões",
        "pontos_turisticos": ["Praia de Boa Viagem", "Instituto Ricardo Brennand", "Marco Zero"],
        "universidade": "Universidade Federal de Pernambuco (UFPE)"
    },
    "Manaus": {
        "população": "2,1 milhões",
        "pontos_turisticos": ["Teatro Amazonas", "Encontro das Águas", "Palácio Rio Negro"],
        "universidade": "Universidade Federal do Amazonas (UFAM)"
    },
    "Natal": {
        "população": "1,4 milhões",
        "pontos_turisticos": ["Forte dos Reis Magos", "Praia de Ponta Negra", "Dunas de Genipabu"],
        "universidade": "Universidade Federal do Rio Grande do Norte (UFRN)"
    },
    "Maceió": {
        "população": "1,0 milhão",
        "pontos_turisticos": ["Praia do Francês", "Palácio Marechal Floriano Peixoto", "Igreja de São Gonçalo do Amarante"],
        "universidade": "Universidade Federal de Alagoas (UFAL)"
    },
    "Cuiabá": {
        "população": "620 mil",
        "pontos_turisticos": ["Parque Nacional de Chapada dos Guimarães", "Catedral Basílica do Senhor Bom Jesus", "Museu do Morro da Caixa D'Água"],
        "universidade": "Universidade Federal de Mato Grosso (UFMT)"
    },
    "Aracaju": {
        "população": "650 mil",
        "pontos_turisticos": ["Praia de Atalaia", "Museu Palácio Marechal Floriano Peixoto", "Mercado Municipal"],
        "universidade": "Universidade Federal de Sergipe (UFS)"
    }
}

# Armazenar histórico de conversas
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Configuração do prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente útil que fornece informações sobre cidades do Brasil."),
    MessagesPlaceholder(variable_name="messages")
])

# Função para buscar informações das cidades
def get_city_info(city):
    if city in city_data:
        info = city_data[city]
        return (f"A cidade de {city} tem uma população de {info['população']}. "
                f"Seus principais pontos turísticos são {', '.join(info['pontos_turisticos'])}. "
                f"A principal universidade é {info['universidade']}.")
    else:
        return "Desculpe, mas não possuo informações sobre a cidade escolhida."

# Pipeline de execução
chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages"))
    | prompt
    | model
)

# Rota da API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id", "default_session")

    # Processar a entrada do usuário
    history = get_session_history(session_id)
    city = next((c for c in city_data if c.lower() in user_input.lower()), None)
    if city:
        response_text = get_city_info(city)
    else:
        response_text = "Por favor, mencione uma cidade válida na sua pergunta."

    # Adicionar ao histórico
    history.add_user_message(user_input)
    history.add_ai_message(response_text)

    # Invocar o modelo
    response = chain.invoke({"messages": history.messages})
    return jsonify({"response": response_text})

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)