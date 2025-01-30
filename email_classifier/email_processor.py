import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Baixar recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Inicializar stemmer e stopwords uma única vez
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Pré-processa um texto removendo pontuações, convertendo para minúsculas,
    tokenizando, removendo stopwords e aplicando stemming.
    """
    if not text or not isinstance(text, str):
        logging.warning("Texto inválido ou vazio recebido para processamento.")
        return ""

    logging.info("Iniciando pré-processamento do texto...")

    # Converter para minúsculas e remover pontuações
    text = text.lower().translate(str.maketrans('', '', string.punctuation))

    # Tokenização
    words = word_tokenize(text, language='english')

    # Remover stop words e aplicar stemming
    processed_words = [ps.stem(word) for word in words if word not in stop_words and not word.isnumeric()]

    processed_text = ' '.join(processed_words)
    logging.info(f"Texto processado: {processed_text}")
    
    return processed_text

# Exemplo de uso
if __name__ == "__main__":
    email_text = "Hi, I would like to inquire about the status of my request. My reference number is 12345!"
    processed_text = preprocess_text(email_text)
    print(f'Texto processado: {processed_text}')
