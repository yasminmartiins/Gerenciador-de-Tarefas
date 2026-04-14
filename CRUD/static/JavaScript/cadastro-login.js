const Toast = Swal.mixin({
    background: '#1e1e1e',
    color: '#ffffff',
    confirmButtonColor: '#4caf5c',
    cancelButtonColor: '#e74c3c'
});

async function efetuarCadastro() {
    const elNome = document.getElementById('nome');
    const elEmail = document.getElementById('email');
    const elCpf = document.getElementById('cpf');
    const elSenha = document.getElementById('senha');

    const nome = elNome.value.trim();
    const email = elEmail.value.trim();
    const cpf = elCpf.value.trim();
    const senha = elSenha.value;
    const rg = document.getElementById('rg').value;
    const tel = document.getElementById('tel').value;
    const status = document.getElementById('status').value;
    const cargo = document.getElementById('cargo').value;

    if (!nome || !email || !senha || !cpf) {
        Toast.fire({
            title: 'Campos Vazios!',
            text: 'Por favor, preencha todos os campos obrigatórios (Nome, CPF, E-mail e Senha).',
            icon: 'info'
        });
        return; 
    }

    const regexCpf = /^\d{11}$|^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
    if (!regexCpf.test(cpf)) {
        elCpf.setCustomValidity("O CPF deve conter 11 dígitos numéricos.");
        elCpf.reportValidity();
        return;
    } else { elCpf.setCustomValidity(""); }

    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexEmail.test(email)) {
        elEmail.setCustomValidity("Por favor, insira um e-mail válido.");
        elEmail.reportValidity();
        return;
    } else { elEmail.setCustomValidity(""); }

    const regexSenha = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&.,])[A-Za-z\d@$!%*#?&.,]{8,}$/;
    if (!regexSenha.test(senha)) {
        elSenha.setCustomValidity("A senha deve ter pelo menos 8 caracteres, com letras, números e símbolos.");
        elSenha.reportValidity(); 
        return;
    } else { elSenha.setCustomValidity(""); }

    const dados = { nome, rg, cpf, tel, email, senha, status, cargo };

    try {
        const response = await fetch('/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (response.ok) {
            Toast.fire({
                title: 'Sucesso!',
                text: resultado.message,
                icon: 'success',
                confirmButtonText: 'Ir para o Login'
            }).then((result) => {
                if (result.isConfirmed) window.location.href = "/login";
            });
        } else {
            Toast.fire({
                title: 'Erro no Cadastro',
                text: resultado.error || "Verifique os dados.",
                icon: 'error'
            });
        }
    } catch (error) {
        Toast.fire({
            title: 'Erro Crítico',
            text: 'Não foi possível conectar ao servidor.',
            icon: 'error'
        });
    }
}

async function efetuarLogin() {
    const emailField = document.getElementById('email');
    const senhaField = document.getElementById('senha');

    const email = emailField.value.trim();
    const senha = senhaField.value.trim();

    if (!email || !senha) {
        Toast.fire({
            title: 'Atenção',
            text: 'Por favor, informe o e-mail e a senha.',
            icon: 'warning'
        });
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
            Toast.fire({
                title: 'Falha no Login',
                text: resultado.error || "Credenciais inválidas.",
                icon: 'error'
            });
            senhaField.value = ""; 
        }
    } catch (error) {
        Toast.fire({
            title: 'Erro de Conexão',
            text: 'Servidor offline ou erro de rede.',
            icon: 'error'
        });
    }
}