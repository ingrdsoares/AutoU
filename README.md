# Email Classifier

Este projeto é uma aplicação web que permite a classificação automática de emails como "Produtivo" ou "Improdutivo" e sugere respostas automáticas com base na categoria identificada. A aplicação suporta entrada de texto manual e upload de arquivos nos formatos `.txt` e `.pdf`.

## Funcionalidades
- **Classificação de e-mails** em `Produtivo` ou `Improdutivo`.
- **Processamento de texto** para limpar e preparar o conteúdo dos e-mails.
- **Geração automática de respostas** com base na categoria classificada.
- **Upload de arquivos** para classificar e-mails em formato `.txt` ou `.pdf`.
- **Interface Web** para envio e classificação de e-mails.

## Estrutura do Projeto
```
EmailClassifier/
│── static/
│   ├── script.js          # Código JavaScript para interatividade no frontend
│── templates/
│   ├── index.html         # Interface do usuário
│── uploads/               # Diretório temporário para arquivos enviados
│── app.py                 # Backend Flask
│── email_processor.py     # Pré-processamento de texto
│── email_classifier.py    # Classificação de e-mails com modelo de IA
│── response_generator.py  # Geração de respostas automáticas
│── requirements.txt       # Dependências do projeto
│── README.md              # Documentação do projeto
```

## Tecnologias Utilizadas
- **Python 3.8+**
- **Flask**: Framework web para Python.
- **Transformers (Hugging Face)**: Modelo de classificação `facebook/bart-large-mnli`.
- **OpenAI API**: Geração de respostas automáticas (opcional).
- **PyMuPDF (fitz)**: Extração de texto de arquivos PDF.
- **NLTK**: Biblioteca para processamento de linguagem natural.
- **HTML, CSS, JavaScript**: Frontend básico para interação do usuário.

## Configuração e Execução
### Pré-requisitos
- Python 3.8+
- Conta na OpenAI com chave API
- Instalar dependências:
```sh
pip install flask flask-cors transformers nltk openai pymupdf
```

### Passo 1: Clonar o Repositório
```sh
git clone https://github.com/ingrdsoares/EmailClassifier.git
cd EmailClassifier
```

### Passo 2: Criar e Ativar um Ambiente Virtual
```sh
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instalar Dependências
```sh
pip install -r requirements.txt
```

### Passo 4: Configurar a Chave da API OpenAI
Crie um arquivo `.env` na raiz do projeto e adicione:
```
OPENAI_API_KEY=your-api-key-here
```
Ou defina a variável de ambiente manualmente:
```sh
export OPENAI_API_KEY=your-api-key-here  # No Windows: set OPENAI_API_KEY=your-api-key-here
```

### Passo 5: Executar o Servidor Flask
```sh
python app.py
```
O servidor estará disponível em `http://127.0.0.1:5000/`.

## Como Usar
1. **Acesse a interface web** pelo navegador.
2. **Digite um e-mail** ou **faça upload de um arquivo .txt ou .pdf**.
3. **Clique para classificar** o e-mail.
4. **Veja a categoria e a resposta sugerida automaticamente**.

## Possíveis Erros e Soluções
### Erro: "Chave da API OpenAI não encontrada"
- Verifique se a variável de ambiente `OPENAI_API_KEY` está definida corretamente.

### Erro: "Erro ao carregar modelo de IA"
- Certifique-se de que todas as dependências foram instaladas corretamente.
- Tente reinstalar o modelo:
  ```sh
  pip install transformers
  ```

### Erro: "Arquivo PDF vazio ou sem texto extraível"
- Alguns PDFs podem conter imagens em vez de texto. Para esses casos, utilize um OCR.

## Contribuição
Sinta-se à vontade para contribuir! Faça um fork do repositório, crie uma branch e envie um pull request.

## Licença
Este projeto está sob a licença MIT.

