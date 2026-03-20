let tarefaAtualId = null;

async function carregarAnexos(id) {
    const listaAnexos = document.getElementById('lista_anexos');

    try {
        const response = await fetch(`/listar_anexos/${id}`);
        const anexos = await response.json();

        listaAnexos.innerHTML = "";
        anexos.forEach(a => {
            const icone = obterIconeArquivo(a.nome);
            const item = `
                <div class="item_lista">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="item_data">${a.data}</span>
                        <div style="display: flex; gap: 5px;">
                            <button onclick="visualizarAnexo('${a.nome}')" class="btn-deletar-item" style="color: #3498db; border-color: rgba(52,152,219,0.3);">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button onclick="confirmarExclusaoAnexo(${a.id})" class="btn-deletar-item">
                                &times;
                            </button>
                        </div>
                    </div>
                    <span>
                        <a href="/static/uploads/${a.nome}" target="_blank" style="text-decoration: none; color: #eee; font-size: 0.85rem;">
                            <i class="fas ${icone}" style="margin-right: 8px; color: #3498db;"></i> ${a.nome}
                        </a>
                    </span>
                </div>`;
            listaAnexos.insertAdjacentHTML('beforeend', item);
        });
    } catch (e) {
        listaAnexos.innerHTML = "Erro ao carregar anexos.";
    }
}

async function abrirModal(titulo, id, func, gestor, descricao, setor) {
    tarefaAtualId = id;

    document.getElementById('modal_titulo').innerText = titulo;
    document.getElementById('modal_setor').innerText = setor;
    document.getElementById('modal_func').innerText = func;
    document.getElementById('modal_gestor').innerText = gestor;
    document.getElementById('modal_descricao').innerText = descricao;

    const listaDiv = document.getElementById('lista_comentarios');
    listaDiv.innerHTML = "Carregando...";

    try {
        const response = await fetch(`/listar_comentarios/${id}`);
        const comentarios = await response.json();

        listaDiv.innerHTML = "";
        comentarios.forEach(c => {
            const item = `
                <div class="item_lista">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="item_data">${c.data}</span>
                        <button onclick="confirmarExclusaoComentario(${c.id})" class="btn-deletar-item" title="Excluir comentário">
                            &times;
                        </button>
                    </div>
                    <span>${c.texto}</span>
                </div>`;
            listaDiv.insertAdjacentHTML('beforeend', item);
        });
    } catch (e) {
        listaDiv.innerHTML = "Erro ao carregar comentários.";
    }

    await carregarAnexos(id);

    document.getElementById('modal_detalhes').style.display = "block";
}

async function adicionarComentario() {
    const txt = document.getElementById('novo_comentario');
    const valorTexto = txt.value.trim();

    if (valorTexto === "" || !tarefaAtualId) return;

    const response = await fetch('/comentar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tarefa_id: tarefaAtualId, texto: valorTexto })
    });

    if (response.ok) {
        txt.value = "";
        recarregarDadosModal();
    }
}

async function adicionarAnexo(input) {
    if (input.files && input.files[0] && tarefaAtualId) {
        const formData = new FormData();
        formData.append('file', input.files[0]);

        const response = await fetch(`/upload_anexo/${tarefaAtualId}`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            input.value = "";
            await carregarAnexos(tarefaAtualId);
        } else {
            alert("Erro ao enviar anexo.");
        }
    }
}

async function confirmarExclusaoComentario(id) {
    if (confirm("Deseja realmente excluir este comentário?")) {
        const response = await fetch(`/deletar_comentario/${id}`, { method: 'DELETE' });
        if (response.ok) {
            recarregarDadosModal();
        }
    }
}

async function confirmarExclusaoAnexo(id) {
    if (confirm("Deseja realmente excluir este anexo?")) {
        const response = await fetch(`/deletar_anexo/${id}`, { method: 'DELETE' });
        if (response.ok) {
            recarregarDadosModal();
        }
    }
}

function fecharModal() {
    document.getElementById('modal_detalhes').style.display = "none";
}

function recarregarDadosModal() {
    const tit = document.getElementById('modal_titulo').innerText;
    const set = document.getElementById('modal_setor').innerText;
    const fun = document.getElementById('modal_func').innerText;
    const ges = document.getElementById('modal_gestor').innerText;
    const desc = document.getElementById('modal_descricao').innerText;
    
    abrirModal(tit, tarefaAtualId, fun, ges, desc, set);
}

function visualizarAnexo(nomeArquivo) {
    const extensao = nomeArquivo.split('.').pop().toLowerCase();
    const url = `/static/uploads/${nomeArquivo}`;
    const container = document.getElementById('container_preview');
    const linkDownload = document.getElementById('link_download_direto');
    
    container.innerHTML = "";
    linkDownload.href = url;

    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extensao)) {
        container.innerHTML = `<img src="${url}" alt="Preview">`;
    } else if (extensao === 'pdf') {
        container.innerHTML = `<iframe src="${url}"></iframe>`;
    } else {
        container.innerHTML = `
            <div style="padding: 40px; text-align: center; color: #888;">
                <i class="fas fa-file-alt fa-4x" style="margin-bottom: 20px;"></i>
                <p>Visualização não disponível para este tipo de arquivo.<br>Use o botão abaixo para baixar.</p>
            </div>`;
    }

    document.getElementById('modal_preview').style.display = "block";
}

function fecharPreview() {
    document.getElementById('modal_preview').style.display = "none";
    document.getElementById('container_preview').innerHTML = ""; 
}

function obterIconeArquivo(nome) {
    const ext = nome.split('.').pop().toLowerCase();
    const icones = {
        'pdf': 'fa-file-pdf',
        'xlsx': 'fa-file-excel',
        'xls': 'fa-file-excel',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'jpg': 'fa-file-image',
        'png': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'txt': 'fa-file-alt'
    };
    return icones[ext] || 'fa-file'; 
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal_detalhes');
    if (event.target == modal) {
        fecharModal();
    }
});