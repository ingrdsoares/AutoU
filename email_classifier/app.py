import nltk
import logging
import os
import fitz  # PyMuPDF para ler PDFs
import time
import glob
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from email_processor import preprocess_text
from email_classifier import classify_email
from response_generator import generate_response

# Configuração do NLTK
nltk.data.path.append(os.path.join(os.path.expanduser("~"), "nltk_data"))
nltk.download('punkt')

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Inicialização do Flask
app = Flask(__name__)
CORS(app)

# Diretório para salvar arquivos temporários
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dicionário para armazenar timestamps dos arquivos
uploaded_files = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_email', methods=['POST'])
def process_email():
    try:
        data = request.get_json()
        email_text = data.get('email_text', '').strip()

        if not email_text:
            return jsonify({'error': 'O campo de texto está vazio!'}), 400

        processed_text = preprocess_text(email_text)
        category, confidence = classify_email(processed_text)
        response = generate_response(category)

        logging.info(f"Email classificado como '{category}' | Confiança: {confidence:.2f}")

        return jsonify({
            'category': category,
            'response': response,
            'confidence': confidence,
            'message': f"O email foi classificado como '{category}' com {confidence * 100:.2f}% de confiança."
        })
    except Exception as e:
        logging.error(f"Erro ao processar email: {str(e)}")
        return jsonify({'error': f'Erro ao processar email: {str(e)}'}), 500

@app.route('/upload_email', methods=['POST'])
def upload_email():
    try:
        if 'email_file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado.'}), 400

        file = request.files['email_file']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in ['txt', 'pdf']:
            return jsonify({'error': 'Formato de arquivo não suportado. Apenas .txt e .pdf são permitidos.'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Armazena o timestamp do upload para remoção futura
        uploaded_files[filepath] = time.time()

        email_text = ''
        time.sleep(1)
        
        if file_extension == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                email_text = f.read()
        elif file_extension == 'pdf':
            with fitz.open(filepath) as doc:
                email_text = '\n'.join([page.get_text("text") for page in doc])

        if not email_text.strip():
            return jsonify({'error': 'Arquivo vazio ou sem texto extraível.'}), 400

        processed_text = preprocess_text(email_text)
        category, confidence = classify_email(processed_text)
        response = generate_response(category)

        logging.info(f"Classificação: {category} | Confiança: {confidence:.2f} | Resposta: {response}")

        return jsonify({
            'category': category,
            'response': response,
            'confidence': confidence,
            'filepath': filepath,  # Retorna o caminho do arquivo para futura remoção
            'message': f"O email foi classificado como '{category}' com {confidence * 100:.2f}% de confiança."
        })
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {str(e)}")
        return jsonify({'error': f'Erro ao processar a requisição: {str(e)}'}), 500

@app.route('/delete_file', methods=['POST'])
def delete_file():
    try:
        data = request.get_json()
        filepath = data.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'Arquivo não encontrado ou já removido.'}), 400

        file_age = time.time() - uploaded_files.get(filepath, 0)

        if file_age < 300:  # 5 minutos
            return jsonify({'error': 'O arquivo só pode ser removido após 5 minutos.'}), 403

        os.remove(filepath)
        uploaded_files.pop(filepath, None)  # Remove do controle interno

        logging.info(f"Arquivo removido manualmente: {filepath}")
        return jsonify({'message': 'Arquivo removido com sucesso.'})
    except Exception as e:
        logging.error(f"Erro ao remover arquivo: {str(e)}")
        return jsonify({'error': f'Erro ao remover arquivo: {str(e)}'}), 500

# Função para remoção automática de arquivos após 5 minutos
def clear_uploads():
    """Remove arquivos que passaram do tempo limite de 5 minutos."""
    current_time = time.time()
    files_to_delete = []

    for filepath, upload_time in list(uploaded_files.items()):
        file_age = current_time - upload_time
        if file_age >= 300:  # 5 minutos = 300 segundos
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logging.info(f"Arquivo removido automaticamente: {filepath}")
                files_to_delete.append(filepath)  # Marca para remoção do dicionário
            except Exception as e:
                logging.error(f"Erro ao remover arquivo {filepath}: {str(e)}")

    # Remove os arquivos do dicionário de controle
    for filepath in files_to_delete:
        uploaded_files.pop(filepath, None)

# Função para agendar a remoção automática de arquivos
def schedule_cleanup():
    clear_uploads()
    threading.Timer(30, schedule_cleanup).start()  # Executa a cada 30 segundos

# Tratamento de erros para garantir que a resposta seja sempre JSON
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Rota não encontrada'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método não permitido'}), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    schedule_cleanup()  # Inicia a limpeza automática
    app.run(debug=True)
