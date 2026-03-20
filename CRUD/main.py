from flask import Flask, render_template, request, redirect, url_for, jsonify
import models
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'xlsx', 'xls', 'doc', 'docx', 'txt', 'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    lista_funcoes = models.listar_funcoes()
    
    return render_template('criar_chamado.html', 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores,
                           funcoes=lista_funcoes)

@app.route('/status')
def status():
    todas = models.listar_todas_tarefas()
    lista_funcs = models.listar_funcionarios()
    lista_gestores = models.listar_gestores()
    lista_funcoes = models.listar_funcoes()
    
    return render_template('status_chamado.html', 
                           tarefas=todas, 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores,
                           funcoes=lista_funcoes)

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
    lista_funcoes = models.listar_funcoes()
    
    return render_template('editar_chamado.html', 
                           tarefa=tarefa_existente, 
                           funcionarios=lista_funcs, 
                           gestores=lista_gestores,
                           funcoes=lista_funcoes)

@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    data = request.get_json()
    models.atualizar_status_tarefa(data['id'], data['status'])
    return jsonify({"success": True})

@app.route('/excluir/<int:id>')
def excluir(id):
    models.excluir_tarefa(id)
    return redirect(url_for('status'))


@app.route('/listar_comentarios/<int:id_tarefa>')
def listar_comentarios_rota(id_tarefa):
    comentarios = models.buscar_comentarios(id_tarefa)
    lista_json = []
    for c in comentarios:
        lista_json.append({
            "id": c['id'],     
            "texto": c['texto'],
            "data": c['data']
        })
    return jsonify(lista_json)

@app.route('/comentar', methods=['POST'])
def comentar_rota():
    dados = request.get_json()
    id_tarefa = dados.get('tarefa_id')
    texto = dados.get('texto')
    
    if id_tarefa and texto:
        models.salvar_comentario(id_tarefa, texto)
        return jsonify({"status": "sucesso"}), 200
    return jsonify({"status": "erro"}), 400

@app.route('/deletar_comentario/<int:id>', methods=['DELETE'])
def deletar_comentario(id):
    models.excluir_comentario(id)
    return jsonify({"success": True})

@app.route('/upload_anexo/<int:id_tarefa>', methods=['POST'])
def upload_anexo(id_tarefa):
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files['file']
    if arquivo.filename == '' or not allowed_file(arquivo.filename):
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    nome_seguro = secure_filename(arquivo.filename)
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
    arquivo.save(caminho)

    models.salvar_anexo(id_tarefa, nome_seguro)
    return jsonify({"status": "sucesso", "arquivo": nome_seguro})

@app.route('/listar_anexos/<int:id_tarefa>')
def listar_anexos(id_tarefa):
    anexos = models.buscar_anexos(id_tarefa)
    lista = [{"id": a['id'], "nome": a['nome_arquivo'], "data": a['data']} for a in anexos]
    return jsonify(lista)

@app.route('/deletar_anexo/<int:id>', methods=['DELETE'])
def deletar_anexo(id):
    nome_arquivo = models.excluir_anexo(id)
    if nome_arquivo:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)