from flask import Flask, render_template, request, redirect, url_for, jsonify
import database
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

with app.app_context():
    database.criar_banco()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        sala_id = request.form.get('sala_id')
        funcionario = request.form.get('funcionario')
        funcao = request.form.get('funcao')
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        prioridade = request.form.get('prioridade').lower() 
        gestor = request.form.get('gestor')

        if sala_id and sala_id != "":
            conn = models.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM salas WHERE id = ?", (sala_id,))
            sala = cursor.fetchone()
            conn.close()
            
            if sala and sala['status'] == 'Indisponível':
                flash("Esta sala está reservada!")
                return redirect(url_for('criar'))
            
            models.reservar_sala(sala_id)
        else:
            sala_id = None
        
        models.inserir_tarefa(sala_id,funcionario, funcao, titulo, descricao, prioridade, gestor)
        return redirect(url_for('status'))

    return render_template('criar_chamado.html', 
                         funcionarios=models.listar_funcionarios(),
                         gestores=models.listar_gestores(),
                         funcoes=models.listar_funcoes(),
                         salas=models.listar_salas())

@app.route('/status')
def status():
    tarefas = models.listar_todas_tarefas()
    return render_template('status_chamado.html', 
                         tarefas=tarefas,
                         funcionarios=models.listar_funcionarios(),
                         gestores=models.listar_gestores(),
                         funcoes=models.listar_funcoes())

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        models.atualizar_tarefa_completa(
            id,
            request.form.get('funcionario'),
            request.form.get('funcao'),
            request.form.get('titulo'),
            request.form.get('descricao'),
            request.form.get('prioridade').lower(),
            request.form.get('gestor'),
            request.form.get('sala_id')
        )
        return redirect(url_for('status'))
    
    tarefa = models.buscar_tarefa_por_id(id)
    return render_template('editar_chamado.html', 
                         tarefa=tarefa,
                         funcionarios=models.listar_funcionarios(),
                         gestores=models.listar_gestores(),
                         funcoes=models.listar_funcoes(),
                         salas=models.listar_salas())

@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    dados = request.get_json()
    if dados:
        models.atualizar_status(dados['id'], dados['status'])
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/excluir/<int:id>')
def excluir(id):
    anexos = models.buscar_anexos(id)
    
    for anexo in anexos:
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], anexo['nome_arquivo'])
        if os.path.exists(caminho):
            os.remove(caminho)
    
    models.excluir_tarefa(id) 
    
    return redirect(url_for('status'))

@app.route('/comentar', methods=['POST'])
def adicionar_comentario():
    dados = request.get_json()
    id_tarefa = dados.get('tarefa_id')
    texto = dados.get('texto')
    
    if id_tarefa and texto:
        models.inserir_comentario(id_tarefa, texto)
        return jsonify({"status": "sucesso"}), 200
    return jsonify({"erro": "Dados inválidos"}), 400

@app.route('/listar_comentarios/<int:id_tarefa>')
def listar_comentarios(id_tarefa):
    comentarios = models.buscar_comentarios(id_tarefa)
    lista = [{"id": c['id'], "texto": c['texto'], "data": c['data']} for c in comentarios]
    return jsonify(lista)

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
        return jsonify({"erro": "Arquivo inválido ou não permitido"}), 400

    nome = secure_filename(arquivo.filename)
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome)
    arquivo.save(caminho)

    models.salvar_anexo(id_tarefa, nome)
    return jsonify({"status": "sucesso", "arquivo": nome})

@app.route('/listar_anexos/<int:id_tarefa>')
def listar_anexos(id_tarefa):
    anexos = models.buscar_anexos(id_tarefa)
    lista = [{"id": a['id'], "nome": a['nome_arquivo'], "data": a['data']} for a in anexos]
    return jsonify(lista)

@app.route('/deletar_anexo/<int:id>', methods=['DELETE'])
def deletar_anexo(id):
    nome_arquivo = models.excluir_anexo(id)
    
    if nome_arquivo:
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
            
    return jsonify({"success": True})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrar.html')

if __name__ == '__main__':
    app.run(debug=True)