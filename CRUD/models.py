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

def salvar_comentario(tarefa_id, texto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comentarios (tarefa_id, texto) VALUES (?, ?)', (tarefa_id, texto))
    conn.commit()
    conn.close()

def buscar_comentarios(tarefa_id):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, texto, datetime(data_hora, 'localtime') as data 
        FROM comentarios 
        WHERE tarefa_id = ? 
        ORDER BY data_hora DESC
    ''', (tarefa_id,))
    colunas = cursor.fetchall()
    conn.close()
    return colunas

def salvar_anexo(tarefa_id, nome_arquivo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO anexos (tarefa_id, nome_arquivo) VALUES (?, ?)', (tarefa_id, nome_arquivo))
    conn.commit()
    conn.close()

def buscar_anexos(tarefa_id):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome_arquivo, datetime(data_hora, 'localtime') as data 
        FROM anexos WHERE tarefa_id = ? 
        ORDER BY data_hora DESC
    ''', (tarefa_id,))
    res = cursor.fetchall()
    conn.close()
    return res
    

def excluir_comentario(id_comentario):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM comentarios WHERE id = ?', (id_comentario,))
    conn.commit()
    conn.close()

def excluir_anexo(id_anexo):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT nome_arquivo FROM anexos WHERE id = ?', (id_anexo,))
    anexo = cursor.fetchone()
    
    if anexo:
        nome_arquivo = anexo['nome_arquivo']
        cursor.execute('DELETE FROM anexos WHERE id = ?', (id_anexo,))
        conn.commit()
        conn.close()
        return nome_arquivo
    conn.close()
    return None