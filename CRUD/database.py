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

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()