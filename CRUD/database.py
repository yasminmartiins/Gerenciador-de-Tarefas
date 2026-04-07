import sqlite3

def conectar():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            rg TEXT,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            status TEXT DEFAULT 'Ativo',
            cargo TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT DEFAULT 'Disponível'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER, -- Dono da tarefa (quem criou)
            sala_id INTEGER,
            funcionario TEXT,   -- Nome de quem vai executar
            funcao TEXT,
            titulo TEXT,
            descricao TEXT,
            prioridade TEXT,
            status TEXT,
            gestor TEXT,        -- Nome do gestor responsável
            data_criacao DATETIME,
            data_conclusao DATETIME,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (sala_id) REFERENCES salas (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa_id INTEGER,
            texto TEXT NOT NULL,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tarefa_id) REFERENCES tarefas (id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anexos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa_id INTEGER,
            nome_arquivo TEXT NOT NULL,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tarefa_id) REFERENCES tarefas (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM funcoes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO funcoes (nome) VALUES (?)", 
                          [('Desenvolvedor',), ('Product Owner',), ('Tech Lead',), ('Scrum Master',)])
        
    cursor.execute("SELECT COUNT(*) FROM salas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO salas (nome) VALUES (?)", 
                          [('Sala de Reunião 01',), ('Auditório',), ('Laboratório',)])

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    criar_banco()