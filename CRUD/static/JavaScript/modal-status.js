function abrirModal(titulo, id, func, gestor, descricao, setor) {
    document.getElementById('modal_titulo').innerText = titulo;
    document.getElementById('modal_setor').innerText = setor;
    document.getElementById('modal_func').innerText = func;
    document.getElementById('modal_gestor').innerText = gestor;
    const campoDesc = document.getElementById('modal_descricao');
    campoDesc.innerText = descricao; 
    
    document.getElementById('modal_detalhes').style.display = "block";
}

function adicionarComentario() {
    const txt = document.getElementById('novo_comentario');
    const lista = document.getElementById('lista_comentarios');
    
    if (txt.value.trim() === "") return;

    const agora = new Date();
    const dataFormatada = agora.toLocaleDateString('pt-BR') + ' ' + agora.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});

    const novoItem = `
        <div class="item_lista">
            <span class="item_data">${dataFormatada}</span>
            <span>${txt.value}</span>
        </div>
    `;

    lista.insertAdjacentHTML('afterbegin', novoItem);
    txt.value = "";
    lista.scrollTop = 0;
}

function adicionarAnexo(input) {
    if (input.files && input.files[0]) {
        const lista = document.getElementById('lista_anexos');
        const agora = new Date();
        const dataFormatada = agora.toLocaleDateString('pt-BR') + ' ' + agora.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});
        const nomeArquivo = input.files[0].name;

        const novoAnexo = `
            <div class="item_lista">
                <span class="item_data">${dataFormatada}</span>
                <span><i class="fas fa-file-alt" style="margin-right: 5px;"></i> ${nomeArquivo}</span>
            </div>
        `;

        lista.insertAdjacentHTML('afterbegin', novoAnexo);
        lista.scrollTop = 0;
    }
}

function fecharModal() {
    const modal = document.getElementById('modal_detalhes');
    modal.style.display = "none";
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modal_detalhes');

    if (event.target == modal) {
        fecharModal();
    }
});