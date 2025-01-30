document.addEventListener('DOMContentLoaded', function () {
  const textForm = document.getElementById('text-form');
  const fileForm = document.getElementById('file-form');
  const resultDiv = document.getElementById('result');
  const categorySpan = document.getElementById('category');
  const replySpan = document.getElementById('reply');
  const loadingDiv = document.getElementById('loading');
  const errorMessageDiv = document.getElementById('error-message');

  // Processar email via texto
  textForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const emailText = document.getElementById('email_text').value.trim();
    console.log('Texto capturado:', emailText); // Debug para verificar se o texto está correto

    if (!emailText) {
      alert('Por favor, insira um texto.');
      return;
    }

    // Limpar mensagens anteriores
    resetMessages();

    await sendEmailData('/process_email', { email_text: emailText });
  });

  // Processar email via upload de arquivo
  fileForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById('email_file');
    if (!fileInput.files.length) {
      alert('Por favor, selecione um arquivo.');
      return;
    }

    // Limpar mensagens anteriores
    resetMessages();

    await sendFileData(fileInput.files[0]);
  });

  // Função para enviar dados do email (texto)
  async function sendEmailData(url, data) {
    showLoading(true);
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Erro HTTP: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      displayResult(result);
    } catch (error) {
      console.error('Erro ao processar:', error);
      showError('Erro ao processar o email: ' + error.message);
    }
    showLoading(false);
  }

  // Função para enviar arquivo de email
  async function sendFileData(file) {
    let formData = new FormData();
    formData.append('email_file', file);

    showLoading(true);
    try {
      let response = await fetch('http://127.0.0.1:5000/upload_email', {
        method: 'POST',
        body: formData,
      });

      let contentType = response.headers.get('content-type');

      if (!contentType || !contentType.includes('application/json')) {
        let textResponse = await response.text(); // Obtém a resposta como texto para depuração
        throw new Error(
          `Resposta do servidor não é JSON válido. Resposta: ${textResponse}`,
        );
      }

      let data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      displayResult(data);
    } catch (error) {
      console.error('Erro ao processar arquivo:', error);
      alert('Erro ao processar arquivo: ' + error.message);
    }
    showLoading(false);
  }

  // Exibir resultados na página
  function displayResult(data) {
    if (data.error) {
      showError(`Erro: ${data.error}`);
      return;
    }

    categorySpan.textContent = data.category;
    replySpan.textContent = data.response;
    resultDiv.style.display = 'block';
  }

  // Exibir ou esconder indicador de carregamento
  function showLoading(show) {
    loadingDiv.style.display = show ? 'block' : 'none';
  }

  // Exibir mensagens de erro
  function showError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = 'block';
  }

  // Resetar mensagens de erro e resultado
  function resetMessages() {
    errorMessageDiv.style.display = 'none';
    resultDiv.style.display = 'none';
  }
});
