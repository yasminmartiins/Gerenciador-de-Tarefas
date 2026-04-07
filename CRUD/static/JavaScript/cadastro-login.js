async function efetuarCadastro() {
    const nome = document.getElementById('nome').value;
    const rg = document.getElementById('rg').value;
    const cpf = document.getElementById('cpf').value;
    const tel = document.getElementById('tel').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    const status = document.getElementById('status').value;
    const cargo = document.getElementById('cargo').value;

    if (!nome || !email || !senha || !cpf) {
        alert("Por favor, preencha todos os campos obrigatórios (Nome, CPF, E-mail e Senha).");
        return;
    }

    const dados = { nome, rg, cpf, tel, email, senha, status, cargo };

    try {
        const response = await fetch('/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (response.ok) {
            alert("Sucesso! " + resultado.message);
            window.location.href = "/login"; 
        } else {
            alert("Erro no cadastro: " + (resultado.error || "Verifique os dados e tente novamente."));
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro crítico: Não foi possível conectar ao servidor.");
    }
}

async function efetuarLogin() {
    const emailField = document.getElementById('email');
    const senhaField = document.getElementById('senha');

    const email = emailField.value.trim();
    const senha = senhaField.value.trim();

    if (!email || !senha) {
        alert("Por favor, informe o e-mail e a senha.");
        return;
    }

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });

        const resultado = await response.json();

        if (response.ok) {
            window.location.href = "/"; 
        } else {
            alert("Falha no Login: " + (resultado.error || "Credenciais inválidas."));
            senhaField.value = ""; 
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro crítico: Não foi possível conectar ao servidor.");
    }
}