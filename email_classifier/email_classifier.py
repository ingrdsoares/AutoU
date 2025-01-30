from transformers import pipeline
import logging
import re

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carregar o pipeline de classificação uma única vez
try:
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    logging.info("Modelo carregado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao carregar modelo: {str(e)}")
    classifier = None

# Mapeamento dos rótulos retornados pelo modelo para os esperados no desafio
LABEL_MAPPING = {
    "produtivo": "Produtivo",
    "improdutivo": "Improdutivo",
}

# Função para limpar e normalizar o texto
def preprocess_text(text):
    text = text.strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove caracteres especiais
    return text

# Função para classificar o email
def classify_email(text):
    if not classifier:
        return "Erro", 0.0  # Retorna erro caso o modelo não tenha carregado

    text = preprocess_text(text)
    if not text:
        return "Erro", 0.0  # Caso o texto esteja vazio

    candidate_labels = ["Produtivo", "Improdutivo"]

    try:
        result = classifier(text, candidate_labels)
        predicted_label = result['labels'][0].lower().strip()  # Normaliza para minúsculas e remove espaços
        confidence = round(result['scores'][0], 4)  # Arredonda a confiança para 4 casas decimais

        # Mapeia para os rótulos corretos
        category = LABEL_MAPPING.get(predicted_label, "Improdutivo")

        return category, confidence
    except Exception as e:
        logging.error(f"Erro ao classificar email: {str(e)}")
        return "Erro", 0.0

# Exemplo de uso
if __name__ == "__main__":
    email_text = "Hi, can you please confirm the status of my order?"
    category, confidence = classify_email(email_text)
    print(f'Categoria: {category}, Confiança: {confidence * 100:.2f}%')
