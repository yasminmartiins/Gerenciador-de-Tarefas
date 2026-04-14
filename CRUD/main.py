from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import database, models, os, sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Dfm39l@49adDffA!'

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        sala_id = request.form.get('sala_id')
        if sala_id == "": sala_id = None
        
        models.inserir_tarefa(
            session['usuario_id'],
            sala_id,
            request.form.get('funcionario'),
            request.form.get('funcao'),
            request.form.get('titulo'),
            request.form.get('descricao'),
            request.form.get('prioridade').lower(),
            request.form.get('gestor')
        )
        return redirect(url_for('status'))

    return render_template('criar_chamado.html', 
                         funcionarios=models.listar_funcionarios(),
                         gestores=models.listar_gestores(),
                         funcoes=models.listar_funcoes(),
                         salas=models.listar_salas())

@app.route('/status')
def status():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    tarefas = models.listar_todas_tarefas(session['usuario_id'])
    return render_template('status_chamado.html', tarefas=tarefas)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        sala_id = request.form.get('sala_id')
        if sala_id == "": sala_id = None

        models.atualizar_tarefa_completa(
            id,
            request.form.get('funcionario'),
            request.form.get('funcao'),
            request.form.get('titulo'),
            request.form.get('descricao'),
            request.form.get('prioridade').lower(),
            request.form.get('gestor'),
            sala_id
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

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dados = request.get_json()
        senha = dados.get('senha')
        
        if not dados.get('email') or not dados.get('senha'):
            return jsonify({"error": "E-mail e senha são obrigatórios"}), 400

        senha_segura = generate_password_hash(senha)

        conn = None

        try:
            conn = database.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, rg, cpf, telefone, email, senha, status, cargo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dados['nome'], dados['rg'], dados['cpf'], 
                dados['tel'], dados['email'], senha_segura, 
                dados['status'], dados['cargo']
            ))
            conn.commit()
            conn.close()
            return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Este CPF ou E-mail já está cadastrado!"}), 400
        except Exception as e:
            return jsonify({"error": f"Erro interno: {str(e)}"}), 500
        
        finally:
            if conn:
                conn.close()

    return render_template('cadastrar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados = request.get_json()
        email = dados.get('email')
        senha_digitada = dados.get('senha')

        conn = database.conectar()
        cursor = conn.cursor()
        usuario = cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()

        if usuario:
            if check_password_hash(usuario['senha'], senha_digitada):
                session['usuario_id'] = usuario['id']
                session['usuario_nome'] = usuario['nome']
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False, "error": "E-mail ou senha incorretos!"}), 401
        
        return jsonify({"success": False, "error": "E-mail ou senha incorretos!"}), 404

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()     
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)