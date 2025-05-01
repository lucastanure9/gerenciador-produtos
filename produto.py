class Produto:
    def __init__(self, id, nome, preco, data_validade=None, descricao=None):
        if not nome or not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if preco is None:
            raise ValueError("Preço não pode ser vazio.")
        self.id = id
        self.nome = nome
        self.preco = preco
        self.data_validade = data_validade
        self.descricao = descricao

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Preço: R${self.preco:.2f}\n"
            f"Validade: {self.data_validade or '-'}\n"
            f"Descrição: {self.descricao or '-'}"
        )
