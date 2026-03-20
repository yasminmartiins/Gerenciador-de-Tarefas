import sqlite3

def criar_banco():
    conexao = sqlite3.connect('app.db')
    cursor = conexao.cursor()

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
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario TEXT NOT NULL,
            funcao TEXT,
            local TEXT,
            tarefa TEXT NOT NULL,
            prioridade TEXT,
            status TEXT DEFAULT 'pendente',
            inicio TEXT,
            termino TEXT,
            responsavel_registro TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
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

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()