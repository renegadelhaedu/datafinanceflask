const express = require('express');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/submit_form', (req, res) => {
    const formData = req.body;

    // Ler o arquivo JSON atual
    let data = [];
    try {
        const jsonData = fs.readFileSync('data.json', 'utf8');
        data = JSON.parse(jsonData);
    } catch (err) {
        console.error('Erro ao ler o arquivo JSON:', err);
    }

    // Adicionar os novos dados ao array
    data.push(formData);

    // Escrever os dados atualizados de volta ao arquivo JSON
    fs.writeFile('data.json', JSON.stringify(data, null, 2), (err) => {
        if (err) {
            console.error('Erro ao escrever no arquivo JSON:', err);
            res.status(500).send('Erro ao processar a solicitação');
            return;
        }
        console.log('Dados salvos com sucesso no arquivo JSON.');
        res.sendStatus(200); // Envio de resposta de sucesso
    });
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
