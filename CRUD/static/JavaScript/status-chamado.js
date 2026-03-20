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
            const painel = document.getElementById('painel_filtros');
            painel.classList.toggle('painel_filtros_visivel');
            painel.classList.toggle('painel_filtros_oculto');
        }

        function filtrarCards() {
            const buscaTexto = document.getElementById('input_busca').value.toLowerCase();
            const filtroFuncionario = document.getElementById('filtro_funcionario').value.toLowerCase();
            const filtroGestor = document.getElementById('filtro_gestor').value.toLowerCase();
            const filtroFuncao = document.getElementById('filtro_funcao').value.toLowerCase();
            const filtroPrioridade = document.getElementById('filtro_prioridade').value.toLowerCase();

            const cards = document.querySelectorAll('.cartao_chamado');

            cards.forEach(card => {
                const titulo = card.querySelector('.titulo_tarefa').innerText.toLowerCase();
                const funcionario = card.querySelector('.nome_func').innerText.toLowerCase();
                const funcao = card.querySelector('.card-funcao').innerText.toLowerCase();
                const gestor = card.querySelector('.card-gestor').innerText.toLowerCase();
                const prioridade = card.querySelector('.prioridade_nivel').classList.contains(filtroPrioridade) || filtroPrioridade === "";

                const bateBusca = titulo.includes(buscaTexto) || funcionario.includes(buscaTexto);
                const bateFuncionario = filtroFuncionario === "" || funcionario.includes(filtroFuncionario);
                const bateGestor = filtroGestor === "" || gestor.includes(filtroGestor);
                const bateFuncao = filtroFuncao === "" || funcao.includes(filtroFuncao);
                const batePrioridade = filtroPrioridade === "" || card.querySelector('.prioridade_nivel').classList.contains(filtroPrioridade);

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

            if (painelFiltro.classList.contains('painel_filtros_visivel')) {
                if (!painelFiltro.contains(event.target) && !botaoFiltro.contains(event.target)) {
                    painelFiltro.classList.remove('painel_filtros_visivel');
                }
            }
        }