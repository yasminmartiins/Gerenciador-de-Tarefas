function allowDrop(ev) { 
    ev.preventDefault(); 
    ev.currentTarget.classList.add('over'); 
}

function dragLeave(ev) { 
    ev.currentTarget.classList.remove('over'); 
}

function drag(ev) { 
    ev.target.classList.add('dragging'); 
    ev.dataTransfer.setData("text", ev.target.id); 
}

function dragEnd(ev) { 
    ev.target.classList.remove('dragging');
    document.querySelectorAll('.coluna_kanban').forEach(col => col.classList.remove('over'));
}

function drop(ev) {
    ev.preventDefault();
    const idCardOriginal = ev.dataTransfer.getData("text"); 
    const card = document.getElementById(idCardOriginal);
    const dropTarget = ev.currentTarget.querySelector('.lista_chamados');
    const novoStatus = ev.currentTarget.id; 

    if (dropTarget && card) {
        dropTarget.appendChild(card);
        
        fetch('/atualizar_status', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id: idCardOriginal.replace('card-', ''), 
                status: novoStatus
            })
        })
        .then(response => response.json())
        .then(res => {
            if (res.success) {
                window.location.reload(); 
            }
        });
    }
}

function toggleFiltro() {
    const painel = document.getElementById('painel_filtros');
    painel.classList.toggle('painel_filtros_visivel');
}

function filtrarCards() {
    const busca = document.getElementById('input_busca').value.toLowerCase();
    const filtroFuncionario = document.getElementById('filtro_funcionario').value;
    const filtroGestor = document.getElementById('filtro_gestor').value;
    const filtroFuncao = document.getElementById('filtro_funcao').value;
    const filtroPrioridade = document.getElementById('filtro_prioridade').value;

    document.querySelectorAll('.cartao_chamado').forEach(card => {
        const titulo = card.querySelector('.titulo_tarefa').innerText.toLowerCase();
        const funcionario = card.querySelector('.nome_func').innerText;
        const gestor = card.querySelector('.card-gestor')?.innerText || "";
        const funcao = card.querySelector('.card-funcao')?.innerText || "";
        const prioridade = card.querySelector('.prioridade_nivel');

        const bateBusca = titulo.includes(busca);
        const bateFuncionario = filtroFuncionario === "" || funcionario.includes(filtroFuncionario);
        const bateGestor = filtroGestor === "" || gestor.includes(filtroGestor);
        const bateFuncao = filtroFuncao === "" || funcao.includes(filtroFuncao);
        const batePrioridade = filtroPrioridade === "" || prioridade.classList.contains(filtroPrioridade);

        if (bateBusca && bateFuncionario && bateGestor && bateFuncao && batePrioridade) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

function limparFiltros() {
    document.getElementById('input_busca').value = "";
    document.getElementById('filtro_prioridade').value = "";
    document.getElementById('filtro_funcionario').value = "";
    document.getElementById('filtro_gestor').value = "";
    document.getElementById('filtro_funcao').value = "";
    filtrarCards();
}

window.onclick = function(event) {
    const painelFiltro = document.getElementById('painel_filtros');
    const botaoFiltro = document.querySelector('.bt_filtro_header');

    if (painelFiltro && painelFiltro.classList.contains('painel_filtros_visivel')) {
        if (!painelFiltro.contains(event.target) && !botaoFiltro.contains(event.target)) {
            painelFiltro.classList.remove('painel_filtros_visivel');
        }
    }
}