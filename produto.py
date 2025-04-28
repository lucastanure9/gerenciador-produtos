class Produto:
    def __init__(self, id, nome, preco, data_validade=None, descricao=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.data_validade = data_validade
        self.descricao = descricao

    def exibir(self):
        print(f"ID: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Preço: R${self.preco:.2f}")
        print(f"Validade: {self.data_validade or '-'}")
        print(f"Descrição: {self.descricao or '-'}")
        print("-" * 30)
