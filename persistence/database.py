import sqlite3
from domain.produto import Produto

DB = 'produtos.db'

def conectar():
    return sqlite3.connect(DB)

def criar_tabela():
    with conectar() as conn:
        conn.executescript(open('./persistence/create_table.sql').read())