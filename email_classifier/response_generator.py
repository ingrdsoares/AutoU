import openai
import os
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Obtendo a chave da API da OpenAI de variáveis de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    logging.error("Chave da API OpenAI não encontrada. Defina a variável de ambiente OPENAI_API_KEY.")

# Respostas pré-definidas para categorias conhecidas
PREDEFINED_RESPONSES = {
    "Produtivo": "Obrigado pelo seu email. (Este email contém uma solicitação técnica. Direcionando ao suporte...)",
    "Improdutivo": "Obrigado pelo seu email. (Este email não requer ação imediata.)"
}

def generate_response(category):
    """
    Gera uma resposta automática com base na categoria do email.
    Se a categoria for conhecida, retorna uma resposta pré-definida.
    Caso contrário, utiliza a API da OpenAI para gerar uma resposta apropriada.
    """
    if category in PREDEFINED_RESPONSES:
        return PREDEFINED_RESPONSES[category]
    
    if not openai.api_key:
        return "Erro: chave da API OpenAI não configurada."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que gera respostas automáticas para emails."},
                {"role": "user", "content": f"Crie uma resposta educada para um email classificado como {category}:"}
            ],
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Erro ao gerar resposta com OpenAI: {str(e)}")
        return "Erro ao gerar resposta automática."

# Exemplo de uso
if __name__ == "__main__":
    category = "Produtivo"  # Exemplo de categoria recebida
    auto_reply = generate_response(category)
    print(f'Resposta sugerida: {auto_reply}')
