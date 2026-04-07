async function efetuarCadastro() {
    const dados = {
        nome: document.getElementById('nome').value,
        rg: document.getElementById('rg').value,
        cpf: document.getElementById('cpf').value,
        tel: document.getElementById('tel').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value,
        status: document.getElementById('status').value,
        cargo: document.getElementById('cargo').value
    };

    if (!dados.email || !dados.senha) {
        alert("Preencha os campos obrigatórios!");
        return;
    }

    try {
        const response = await fetch('/cadastrar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (response.ok) {
            alert(resultado.message);
            window.location.href = "/login";
        } else {
            alert("Erro: " + resultado.error);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao conectar com o servidor.");
    }
}

async function efetuarLogin() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    if (!email || !senha) {
        alert("Preencha e-mail e senha!");
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
            alert("Bem-vindo!");
            window.location.href = "/";
        } else {
            alert("Erro: " + resultado.error);
        }
    } catch (error) {
        alert("Erro ao conectar com o servidor.");
    }
}