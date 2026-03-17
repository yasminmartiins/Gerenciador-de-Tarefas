from flask import Flask, render_template, request, redirect, url_for, jsonify
import models

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        funcionario = request.form.get('funcionario')
        funcao = request.form.get('funcao')
        local = request.form.get('local')
        tarefa = request.form.get('tarefa')
        prioridade = request.form.get('prioridade').lower() 
        gestor = request.form.get('gestor')
        
        models.inserir_tarefa(funcionario, funcao, local, tarefa, prioridade, gestor)
        return redirect(url_for('status'))
    
    lista_funcs = models.listar_funcionarios()
    lista_gestores = models.listar_gestores()
    
    return render_template('criar_chamado.html', 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores)

@app.route('/status')
def status():
    todas = models.listar_todas_tarefas()
    lista_funcs = models.listar_funcionarios()
    lista_gestores = models.listar_gestores()
    
    return render_template('status_chamado.html', 
                           tarefas=todas, 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        funcionario = request.form.get('funcionario')
        funcao = request.form.get('funcao')
        local = request.form.get('local')
        tarefa = request.form.get('tarefa')
        prioridade = request.form.get('prioridade').lower()
        gestor = request.form.get('gestor')
        
        models.atualizar_tarefa_completa(id, funcionario, funcao, local, tarefa, prioridade, gestor)
        return redirect(url_for('status'))

    tarefa_existente = models.buscar_tarefa_por_id(id)
    lista_funcs = models.listar_funcionarios()
    lista_gestores = models.listar_gestores()
    
    return render_template('editar_chamado.html', 
                           tarefa=tarefa_existente, 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores)

@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    data = request.get_json()
    models.atualizar_status_tarefa(data['id'], data['status'])
    return jsonify({"success": True})

@app.route('/excluir/<int:id>')
def excluir(id):
    models.excluir_tarefa(id)
    return redirect(url_for('status'))

if __name__ == "__main__":
    app.run(debug=True)