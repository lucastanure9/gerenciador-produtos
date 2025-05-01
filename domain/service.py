from domain.produto import Produto
from persistence.database import conectar


def listar_produtos() -> str:
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM produtos").fetchall()
    if not rows:
        return "Nenhum produto cadastrado."
    lista = [str(Produto(*r)) for r in rows]
    return "=== Lista de Produtos ===\n" + "\n\n".join(lista)


def buscar_por_id(_id: int) -> str:
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (_id,)
        ).fetchone()
    if not row:
        return "Produto não encontrado."
    return "=== Produto Encontrado ===\n" + str(Produto(*row))


def cadastrar_produto(
    nome: str,
    preco: float,
    data_validade: str | None,
    descricao: str | None
) -> str:
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO produtos(nome, preco, data_validade, descricao) VALUES(?,?,?,?)",
                (nome, preco, data_validade, descricao)
            )
        return "Produto cadastrado com sucesso!"
    except Exception:
        return "Falha ao cadastrar produto."


def atualizar_produto(
    _id: int,
    nome: str | None,
    preco: float | None,
    data_validade: str | None,
    descricao: str | None
) -> str:
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (_id,)
        ).fetchone()
        if not row:
            return "Produto não encontrado."
        current = Produto(*row)
        nome = nome or current.nome
        preco = preco if preco is not None else current.preco
        data_validade = data_validade if data_validade is not None else current.data_validade
        descricao = descricao if descricao is not None else current.descricao
        conn.execute(
            "UPDATE produtos SET nome=?, preco=?, data_validade=?, descricao=? WHERE id=?",
            (nome, preco, data_validade, descricao, _id)
        )
    return "Produto atualizado com sucesso!"


def deletar_produto(_id: int) -> str:
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (_id,)
        ).fetchone()
        if not row:
            return "Produto não encontrado."
        conn.execute("DELETE FROM produtos WHERE id=?", (_id,))
    return "Produto deletado com sucesso!"