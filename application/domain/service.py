import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from application.domain.produto import Produto
from application.persistence.database import conectar

def banco_esta_vazio():
    return listar_produtos() == "Nenhum produto cadastrado."

def listar_produtos() -> str:
    
    """
    Lista todos os produtos cadastrados no banco.

    :return: mensagem indicando ausência de produtos ou uma lista formatada com todos os produtos.
    """
    
    with conectar() as conn:
        rows = conn.execute("SELECT * FROM produtos").fetchall()
    if not rows:
        logging.info("Listagem de produtos: nenhum produto encontrado.")
        return "Nenhum produto cadastrado."
    logging.info(f"Listagem de produtos: {len(rows)} encontrados.")
    lista = [str(Produto(*linha)) for linha in rows]
    return "=== Lista de Produtos ===\n" + "\n\n".join(lista)

def buscar_por_id(produto_id: int) -> str:
    
    """
    Busca um produto pelo seu ID.

    :param produto_id: identificador numérico do produto
    :return: string formatada com os dados do produto ou mensagem de não encontrado
    """
    
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()
    if not row:
        logging.warning(f"Produto não encontrado (id={produto_id})")
        return "Produto não encontrado."
    logging.info(f"Produto encontrado (id={produto_id})")
    return "=== Produto Encontrado ===\n" + str(Produto(*row))

def cadastrar_produto(nome: str,preco: float,data_validade: str | None,descricao: str | None) -> str:
    
    """
    Cadastra um novo produto no banco.

    :param nome: nome do produto (obrigatório)
    :param preco: valor do produto (obrigatório)
    :param data_validade: data de validade no formato 'DD-MM-AAAA' (opcional)
    :param descricao: descrição adicional (opcional)
    :return: mensagem de sucesso ou falha no cadastro
    """
    
    try:
        with conectar() as conn:
            conn.execute(
                "INSERT INTO produtos(nome, preco, data_validade, descricao) VALUES(?,?,?,?)",
                (nome, preco, data_validade, descricao)
            )
        logging.info(f"Produto cadastrado: nome={nome}, preco={preco}, validade={data_validade}, descricao={descricao}")
        return "Produto cadastrado com sucesso!"
    except Exception as e:
        logging.error(f"Erro ao cadastrar produto: {e}")
        return "Falha ao cadastrar produto."

def atualizar_produto(produto_id: int,nome: str | None,preco: float | None,data_validade: str | None,descricao: str | None) -> str:
    
    """
    Atualiza os campos de um produto existente.

    :param produto_id: ID do produto a atualizar
    :param nome: novo nome (None para manter atual)
    :param preco: novo preço    (None para manter atual)
    …
    :return: mensagem de sucesso ou produto não encontrado
    """
    
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()
        if not row:
            logging.warning(f"Tentativa de atualizar produto inexistente (id={produto_id})")
            return "Produto não encontrado."
        current = Produto(*row)
        nome = nome or current.nome
        preco = preco if preco is not None else current.preco
        data_validade = data_validade if data_validade is not None else current.data_validade
        descricao = descricao if descricao is not None else current.descricao
        conn.execute(
            "UPDATE produtos SET nome=?, preco=?, data_validade=?, descricao=? WHERE id=?",
            (nome, preco, data_validade, descricao, produto_id)
        )
    logging.info(f"Produto atualizado (id={produto_id}): nome={nome}, preco={preco}, validade={data_validade}, descricao={descricao}")
    return "Produto atualizado com sucesso!"

def deletar_produto(produto_id: int) -> str:
    
    """
    Remove um produto do banco com base no ID informado.

    :param produto_id: identificador do produto a ser removido
    :return: mensagem de sucesso ou de produto não encontrado
    """
    
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ?", (produto_id,)
        ).fetchone()
        if not row:
            logging.warning(f"Tentativa de deletar produto inexistente (id={produto_id})")
            return "Produto não encontrado."
        conn.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
    logging.info(f"Produto deletado (id={produto_id})")
    return "Produto deletado com sucesso!"
