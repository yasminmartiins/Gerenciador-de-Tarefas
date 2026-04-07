import sqlite3

def conectar():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gestores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL           
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            status TEXT DEFAULT 'Disponível' -- 'Disponível' ou 'Indisponível'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sala_id INTEGER,
            funcionario TEXT,
            funcao TEXT,
            titulo TEXT,
            descricao TEXT,
            prioridade TEXT,
            status TEXT,
            gestor TEXT,
            data_criacao DATETIME,
            data_conclusao DATETIME,
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

    cursor.execute("SELECT COUNT(*) FROM funcionarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO funcionarios (nome) VALUES (?)", 
                          [('Carlos Silva',), ('Yasmin Martins',), ('Marcos Oliveira',), ('Bruna Cabral',)])
        
    cursor.execute("SELECT COUNT(*) FROM gestores")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO gestores (nome) VALUES (?)", 
                          [('Ana Souza',), ('Ricardo Santos',), ('Fernando Costa',), ('Leticia Almeida',)])
    
    cursor.execute("SELECT COUNT(*) FROM funcoes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO funcoes (nome) VALUES (?)", 
                          [('Desenvolvedor',), ('Product Owner',), ('Tech Lead',), ('Scrum Master',)])
        
    cursor.execute("SELECT COUNT(*) FROM salas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO salas (nome) VALUES (?)", 
                        [('Sala de Reunião 01',), ('Auditório Principal',), ('Sala de Inovação',)])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()