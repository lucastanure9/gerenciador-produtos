import os
import sqlite3
import tempfile
import pytest

from domain.service import (
    listar_produtos,
    cadastrar_produto,
    buscar_por_id,
    atualizar_produto,
    deletar_produto
)

@pytest.fixture(autouse=True)
def banco_limpo():
    # Criar arquivo temporário e fechá-lo para evitar erro de permissão no Windows
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp_path = tmp.name
    tmp.close()

    os.environ["DB_PATH"] = tmp_path

    with sqlite3.connect(tmp_path) as conn:
        conn.execute("""
            CREATE TABLE produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                data_validade TEXT,
                descricao TEXT
            )
        """)
        conn.commit()

    yield

    try:
        os.unlink(tmp_path)
    except PermissionError:
        pass  # Em último caso, ignore (não recomendado em produção)

def test_listar_produtos_vazio():
    assert listar_produtos() == "Nenhum produto cadastrado."

def test_cadastrar_e_listar():
    cadastrar_produto("Caneta", 2.5, "01-01-2026", "Preta")
    resultado = listar_produtos()
    assert "Caneta" in resultado
    assert "R$2.50" in resultado

def test_buscar_por_id_existente():
    cadastrar_produto("Lápis", 1.0, None, None)
    produto = buscar_por_id(1)
    assert "Lápis" in produto

def test_buscar_por_id_inexistente():
    resultado = buscar_por_id(999)
    assert resultado == "Produto não encontrado."

def test_atualizar_produto_existente():
    cadastrar_produto("Caderno", 10.0, None, "A4")
    msg = atualizar_produto(1, "Caderno Espiral", None, None, None)
    assert "sucesso" in msg.lower()
    atualizado = buscar_por_id(1)
    assert "Caderno Espiral" in atualizado

def test_atualizar_produto_inexistente():
    msg = atualizar_produto(999, "X", None, None, None)
    assert msg == "Produto não encontrado."

def test_deletar_produto_existente():
    cadastrar_produto("Borracha", 1.2, None, "Branca")
    msg = deletar_produto(1)
    assert "sucesso" in msg.lower()
    msg2 = buscar_por_id(1)
    assert msg2 == "Produto não encontrado."

def test_deletar_produto_inexistente():
    msg = deletar_produto(999)
    assert msg == "Produto não encontrado."

def test_formatacao_produto():
    cadastrar_produto("Café", 9.99, "25-12-2025", "Tradicional")
    resultado = buscar_por_id(1)
    assert "ID: 1" in resultado
    assert "Nome: Café" in resultado
    assert "Preço: R$9.99" in resultado
    assert "Validade: 25-12-2025" in resultado
    assert "Descrição: Tradicional" in resultado

def test_formatacao_produto_com_dados_nulos():
    cadastrar_produto("Água", 1.0, None, None)
    resultado = buscar_por_id(1)
    assert "Validade: -" in resultado
    assert "Descrição: -" in resultado