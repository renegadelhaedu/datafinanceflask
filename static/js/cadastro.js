document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar o envio padrão do formulário

    // Obter os valores dos campos do formulário
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const estado = document.getElementById('estado').value;
    const profissao = document.getElementById('profissao').value;
    const senha = document.getElementById('senha').value;

    // Construir um objeto com os dados do formulário
    const formData = {
        nome,
        email,
        estado,
        profissao,
        senha
    };

    // Enviar os dados para o servidor
    fetch('/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            alert('Cadastro realizado com sucesso!');
        } else {
            alert('Ocorreu um erro durante o cadastro.');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Ocorreu um erro durante o cadastro.');
    });
});
