from persistence.database import criar_tabela
from domain.service import (
    listar_produtos,
    buscar_por_id,
    cadastrar_produto,
    atualizar_produto,
    deletar_produto
)
from domain.validation import validar_int, validar_nome, validar_preco, validar_data, OperationCancelled


def menu():
    criar_tabela()

    def solicitar_input(prompt, validator, permitir_vazio=False):
        """Prompt repetido até ter valor válido ou o usuário digitar 'sair'.
    - prompt: string para input()
    - validator: função que recebe string, retorna valor convertido ou None
    - permitir_vazio: se True, ENTER vazio retorna None sem validar
        """

        while True:
            txt = input(prompt).strip()
            if txt.lower() == 'sair':
                raise OperationCancelled()
            if permitir_vazio and txt == '':
                return None
            val = validator(txt)
            if val is not None:
                return val
            print("Entrada inválida. Tente novamente ou digite 'sair' para cancelar.")

    # wrappers para coletar inputs e chamar os serviços com parâmetros
    def opcao_listar():
        mensagem = listar_produtos()
        print(mensagem)

    def opcao_buscar():
        try:
            _id = solicitar_input("ID do produto (ou 'sair'): ", validar_int)
        except OperationCancelled:
            return
        mensagem = buscar_por_id(_id)
        print(mensagem)

    def opcao_cadastrar():
        try:
            nome = solicitar_input("Nome: ", validar_nome)
            preco = solicitar_input("Preço: ", validar_preco)
            data  = solicitar_input(
                "Validade DD-MM-AAAA [opcional]: ", validar_data, permitir_vazio=True
            )
            desc  = solicitar_input(
                "Descrição [opcional]: ", lambda t: t.strip(), permitir_vazio=True
            )
        except OperationCancelled:
            print("Cadastro cancelado.")
            return
        mensagem = cadastrar_produto(nome, preco, data, desc)
        print(mensagem)

    def opcao_atualizar():
        try:
            _id = solicitar_input("ID do produto a atualizar (ou 'sair'): ", validar_int)
        except OperationCancelled:
            return
        try:
            nome = solicitar_input("Nome [opcional]: ", validar_nome, permitir_vazio=True)
            preco = solicitar_input("Preço [opcional]: ", validar_preco, permitir_vazio=True)
            data  = solicitar_input(
                "Validade DD-MM-AAAA [opcional]: ", validar_data, permitir_vazio=True
            )
            desc  = solicitar_input(
                "Descrição [opcional]: ", lambda t: t.strip(), permitir_vazio=True
            )
        except OperationCancelled:
            print("Atualização cancelada.")
            return
        mensagem = atualizar_produto(_id, nome, preco, data, desc)
        print(mensagem)

    def opcao_deletar():
        try:
            _id = solicitar_input("ID do produto a deletar (ou 'sair'): ", validar_int)
        except OperationCancelled:
            return
        mensagem = deletar_produto(_id)
        print(mensagem)

    acoes = {
        '1': opcao_listar,
        '2': opcao_buscar,
        '3': opcao_cadastrar,
        '4': opcao_atualizar,
        '5': opcao_deletar,
    }

    while True:
        print("""
=== MENU ===
1. Listar produtos
2. Buscar por ID
3. Cadastrar novo
4. Atualizar existente
5. Deletar
6. Sair
""")
        escolha = input("Opção: ").strip()
        if escolha == '6':
            break
        acao = acoes.get(escolha)
        if acao:
            acao()
        else:
            print("Opção inválida.")


if __name__ == '__main__':
    menu()