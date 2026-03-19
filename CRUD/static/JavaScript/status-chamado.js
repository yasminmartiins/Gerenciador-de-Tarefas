function allowDrop(ev) { ev.preventDefault(); ev.currentTarget.classList.add('over'); }
        function dragLeave(ev) { ev.currentTarget.classList.remove('over'); }
        function drag(ev) { ev.target.classList.add('dragging'); ev.dataTransfer.setData("text", ev.target.id); }
        function dragEnd(ev) { 
            ev.target.classList.remove('dragging');
            document.querySelectorAll('.coluna_kanban').forEach(col => col.classList.remove('over'));
        }
        function drop(ev) {
            ev.preventDefault();
            const data = ev.dataTransfer.getData("text");
            const card = document.getElementById(data);
            const dropTarget = ev.currentTarget.querySelector('.lista_chamados');
            const novoStatus = ev.currentTarget.id;

            if (dropTarget && card) {
                dropTarget.appendChild(card);
                fetch('/atualizar_status', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id: data.replace('card-', ''), status: novoStatus})
                });
            }
            ev.currentTarget.classList.remove('over');
        }

        function toggleFiltro() {
            document.getElementById('painel_filtros').classList.toggle('painel_filtros_visivel');
        }

        function filtrarCards() {
            const termoBusca = document.getElementById('input_busca').value.toLowerCase();
            const prioFiltro = document.getElementById('filtro_prioridade').value.toLowerCase();
            const funcFiltro = document.getElementById('filtro_funcionario').value.toLowerCase();
            const gestFiltro = document.getElementById('filtro_gestor').value.toLowerCase();
            const funcaoFiltro = document.getElementById('filtro_funcao').value.toLowerCase();
            
            const cards = document.querySelectorAll('.cartao_chamado');

            cards.forEach(card => {
                const descricao = card.querySelector('.titulo_tarefa').innerText.toLowerCase();
                const nomeFunc = card.querySelector('.nome_func').innerText.toLowerCase();
                const nomeGest = card.querySelector('.info_detalhes').innerText.toLowerCase(); 
                
                const bateBusca = descricao.includes(termoBusca);
                const batePrio = prioFiltro === "" || card.querySelector('.prioridade_nivel').classList.contains(prioFiltro);
                const bateFunc = funcFiltro === "" || nomeFunc.includes(funcFiltro);
                const bateGest = gestFiltro === "" || nomeGest.includes(gestFiltro);
                const bateFuncao = funcaoFiltro === "" || card.querySelector('.info_detalhes').classList.contains(funcaoFiltro);

                if (bateBusca && batePrio && bateFunc && bateGest && bateFuncao) {
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

            if (painelFiltro.classList.contains('painel_filtros_visivel')) {
                if (!painelFiltro.contains(event.target) && !botaoFiltro.contains(event.target)) {
                    painelFiltro.classList.remove('painel_filtros_visivel');
                }
            }
        }