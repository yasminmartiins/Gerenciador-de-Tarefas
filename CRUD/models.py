import sqlite3

def conectar():
    return sqlite3.connect('app.db')

def inserir_tarefa(funcionario, funcao, local, tarefa, prioridade, responsavel):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tarefas (funcionario, funcao, local, tarefa, prioridade, status, responsavel_registro)
        VALUES (?, ?, ?, ?, ?, 'pendente', ?)
    ''', (funcionario, funcao, local, tarefa, prioridade, responsavel))
    conn.commit()
    conn.close()

def listar_todas_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_tarefa_por_id(id_tarefa):
    conn = conectar()
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id_tarefa,))
    dado = cursor.fetchone()
    conn.close()
    return dado

def atualizar_tarefa_completa(id_tarefa, funcionario, funcao, local, tarefa, prioridade, gestor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas 
        SET funcionario = ?, funcao = ?, local = ?, tarefa = ?, prioridade = ?, responsavel_registro = ?
        WHERE id = ?
    ''', (funcionario, funcao, local, tarefa, prioridade, gestor, id_tarefa))
    conn.commit()
    conn.close()

def atualizar_status_tarefa(id_tarefa, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    status_limpo = novo_status.replace('col-', '')
    cursor.execute('UPDATE tarefas SET status = ? WHERE id = ?', (status_limpo, id_tarefa))
    conn.commit()
    conn.close()

def excluir_tarefa(id_tarefa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
    conn.commit()
    conn.close()

def listar_funcoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM funcoes ORDER BY nome ASC')
    nomes = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return nomes

def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM funcionarios ORDER BY nome ASC')
    nomes = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return nomes

def listar_gestores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM gestores ORDER BY nome ASC')
    nomes = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return nomes