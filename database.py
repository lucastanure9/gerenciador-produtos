import sqlite3
from produto import Produto
from utils import (
    OperationCancelled, solicitar_input,
    validar_int, validar_nome, validar_preco, validar_data
)

DB = 'produtos.db'

def conectar():
    return sqlite3.connect(DB)

def criar_tabela():
    with conectar() as conn:
        conn.executescript(open('create_table.sql').read())

def listar_produtos():
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM produtos").fetchall()
    if not rows:
        print("Nenhum produto cadastrado.")
    else:
        print("\n=== Lista de Produtos ===")
        for r in rows:
            Produto(*r).exibir()

def buscar_por_id():
    try:
        _id = solicitar_input("ID do produto (ou 'sair'): ", validar_int)
    except OperationCancelled:
        return
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (_id,)
        ).fetchone()
    if row:
        print("\n=== Produto Encontrado ===")
        Produto(*row).exibir()
    else:
        print("Produto não encontrado.")

def cadastrar_produto():
    try:
        nome = solicitar_input("Nome: ", validar_nome)
        preco = solicitar_input("Preço: ", validar_preco)
        data = solicitar_input(
            "Validade DD-MM-AAAA [opcional]: ",
            validar_data, permitir_vazio=True
        )
        desc = solicitar_input(
            "Descrição [opcional]: ",
            lambda t: t.strip(), permitir_vazio=True
        )
    except OperationCancelled:
        print("Cadastro cancelado.")
        return
    with conectar() as conn:
        conn.execute(
            "INSERT INTO produtos(nome, preco, data_validade, descricao) VALUES(?,?,?,?)",
            (nome, preco, data, desc)
        )
    print("Produto cadastrado com sucesso!")

def atualizar_produto():
    try:
        _id = solicitar_input("ID do produto a atualizar (ou 'sair'): ", validar_int)
    except OperationCancelled:
        return
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (_id,)
        ).fetchone()
    if not row:
        print("Produto não encontrado.")
        return

    print("Deixe em branco para manter o valor atual, ou digite 'sair' para cancelar.")
    try:
        nome = solicitar_input(f"Nome [{row[1]}]: ", validar_nome)
        preco = solicitar_input(f"Preço [{row[2]}]: ", validar_preco)
        data = solicitar_input(
            f"Validade [{row[3] or '-'}] DD-MM-AAAA: ",
            validar_data, permitir_vazio=True
        )
        desc = solicitar_input(
            f"Descrição [{row[4] or '-'}]: ",
            lambda t: t.strip(), permitir_vazio=True
        )
    except OperationCancelled:
        print("Atualização cancelada.")
        return

    nome = nome or row[1]
    preco = preco if preco is not None else row[2]
    data = data if data is not None else row[3]
    desc = desc if desc is not None else row[4]

    with conectar() as conn:
        conn.execute(
            "UPDATE produtos SET nome=?, preco=?, data_validade=?, descricao=? WHERE id=?",
            (nome, preco, data, desc, _id)
        )
    print("Produto atualizado com sucesso!")

def deletar_produto():
    try:
        _id = solicitar_input("ID do produto a deletar (ou 'sair'): ", validar_int)
    except OperationCancelled:
        return
    with conectar() as conn:
        conn.execute("DELETE FROM produtos WHERE id=?", (_id,))
    print("Produto deletado.")
