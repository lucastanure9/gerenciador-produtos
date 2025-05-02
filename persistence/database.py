import sqlite3
import os
from domain.produto import Produto

DB = 'produtos.db'

def conectar():
    db_path = os.getenv("DB_PATH", "produtos.db")
    return sqlite3.connect(db_path)

def criar_tabela():
    with conectar() as conn:
        conn.executescript(open('./persistence/create_table.sql').read())