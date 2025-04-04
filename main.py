# Importação das Bibliotecas necessárias
import os
from dotenv import load_dotenv, find_dotenv # Biblioteca para carregar variáveis de ambiente
from langchain_groq import ChatGroq # Integração do LangChain com Groq
from langchain_community.chat_message_histories import ChatMessageHistory #Permite criar histórico de MSG
from langchain_core.chat_history import BaseChatMessageHistory #Cria uma classe base para histórioc de MSG
from langchain_core.runnables.history import RunnableWithMessageHistory #Permite Gerenciar o histórico de MSG
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder #Permite criar prompts e MSG
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages #MSG Humanas, sistema e do AI
from langchain_core.runnables import RunnablePassthrough #Permite criar fluxos de execução e reutilizaveis
from operator import itemgetter #Permite a extração de valores de dicionários

# Carregar as variáveis de ambinete do arquivo .env (para proteger as credenciais)
#load_dotenv()

# Obter a chave da API do Groq que está armazenada no arquivo .env
load_dotenv(find_dotenv())
groq_api_key = os.getenv("GROQ_API_KEY")

# Inicializar o modelo AI
model = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key = groq_api_key
)

# Dicionário de dados de algumas cidades Brasileiras com as seguintes informações:
# População, pontos turísticos e principais universidades
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

# Armazenar para manter o histórico de conversas de cada sessão
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store: # Cria histórico se a sessão não existir ou recupera
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Cria um gerenciador de histórico
with_message_history = RunnableWithMessageHistory(model, get_session_history)

# Configuração do Template e System Message
prompt = ChatPromptTemplate.from_messages([
    # Mensagem do sistema
    ("system", "Você é um assistente útil que fornece informações sobre cidades do Brasil."), 
    # Reserva de espaço para histórico dinâmico das conversas
    MessagesPlaceholder(variable_name="messages")
])
# Função para buscar informações das cidades
def get_city_info(city):
    if city in city_data:
        info = city_data[city]
        return(f"A cidade de {city} tem uma população de {info['população']}. "
                f"Seus principais pontos turísticos são {', '.join(info['pontos_turisticos'])}. "
                f"A principal universidade é {info['universidade']}.")
    else:
        return " Desculpe, mas não possuo informações sobre a cidade escolhida"
    
trimmer = trim_messages(
    max_tokens=4500, # Limite e capacidade máxima de tokens
    strategy="last", # Mantém as últimas interações
    token_counter=model, # Contagem de tokens com o método do Modelo
    include_system=True, #  Inclui a mensagem do sistema no histórico
    allow_partial=False, # Evita que as mensagens fiquem cortadas
    start_on="human" # O início da contagem é feito com mensagens humanas
)

# Pipeline de execução
chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)
    | prompt # Utiliza o template do Prompt
    | model # Envia para o modelo Groq
)

# Exemplo de interação com o chatbot
session_id = "usuario1"
history = get_session_history(session_id)
user_input = "Qual é a população de Belo Horizonte?"
city = "Belo Horizonte"
response_text = get_city_info(city)
history.add_user_message(user_input)
history.add_ai_message(response_text)

# Exibir resposta
echo_response = chain.invoke({
    "messages": history.messages,
})
print("Chatbot:", response_text)