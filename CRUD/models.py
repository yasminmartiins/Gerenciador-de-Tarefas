import sqlite3
import os

def conectar():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def inserir_tarefa(funcionario, funcao, titulo, descricao, prioridade, gestor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (funcionario, funcao, titulo, descricao, prioridade, status, gestor, data_criacao)
        VALUES (?, ?, ?, ?, ?, 'pendente', ?, datetime('now', 'localtime'))
    ''', (funcionario, funcao, titulo, descricao, prioridade, gestor))
    conn.commit()
    conn.close()

def listar_todas_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT *, datetime(data_criacao) as data_criacao FROM tarefas")
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_tarefa_por_id(id_tarefa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id_tarefa,))
    dado = cursor.fetchone()
    conn.close()
    return dado

def atualizar_tarefa_completa(id_tarefa, funcionario, funcao, titulo, descricao, prioridade, gestor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tarefas 
        SET funcionario = ?, funcao = ?, titulo = ?, descricao = ?, prioridade = ?, gestor = ?
        WHERE id = ?
    ''', (funcionario, funcao, titulo, descricao, prioridade, gestor, id_tarefa))
    conn.commit()
    conn.close()

def atualizar_status(id_tarefa, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    if novo_status == 'concluido':
        cursor.execute('''
            UPDATE tarefas 
            SET status = ?, data_conclusao = datetime('now', 'localtime') 
            WHERE id = ?
        ''', (novo_status, id_tarefa))
    else:
        cursor.execute('UPDATE tarefas SET status = ?, data_conclusao = NULL WHERE id = ?', (novo_status, id_tarefa))
    conn.commit()
    conn.close()

def excluir_tarefa(id_tarefa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
    conn.commit()
    conn.close()

def listar_funcionarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM funcionarios')
    res = [row['nome'] for row in cursor.fetchall()]
    conn.close()
    return res

def listar_gestores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM gestores')
    res = [row['nome'] for row in cursor.fetchall()]
    conn.close()
    return res

def listar_funcoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM funcoes')
    res = [row['nome'] for row in cursor.fetchall()]
    conn.close()
    return res

def inserir_comentario(tarefa_id, texto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comentarios (tarefa_id, texto) VALUES (?, ?)', (tarefa_id, texto))
    conn.commit()
    id_gerado = cursor.lastrowid
    conn.close()
    return id_gerado

def buscar_comentarios(tarefa_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, texto, datetime(data_hora, 'localtime') as data 
        FROM comentarios 
        WHERE tarefa_id = ? 
        ORDER BY data_hora DESC
    ''', (tarefa_id,))
    coments = cursor.fetchall()
    conn.close()
    return coments

def salvar_anexo(tarefa_id, nome_arquivo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO anexos (tarefa_id, nome_arquivo) VALUES (?, ?)', (tarefa_id, nome_arquivo))
    conn.commit()
    conn.close()

def buscar_anexos(tarefa_id):
    conn = conectar()
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
    cursor = conn.cursor()
    cursor.execute('SELECT nome_arquivo FROM anexos WHERE id = ?', (id_anexo,))
    arquivo = cursor.fetchone()

    if arquivo:
        nome_arquivo = arquivo['nome_arquivo']
        cursor.execute('DELETE FROM anexos WHERE id = ?', (id_anexo,))
        conn.commit()
        conn.close()
        return nome_arquivo 
    
    conn.close()
    return None