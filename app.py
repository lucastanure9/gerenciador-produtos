from persistence.database import criar_tabela

from domain.service import (
    listar_produtos,
    buscar_por_id,
    cadastrar_produto,
    atualizar_produto,
    deletar_produto
)

def menu():
    criar_tabela()
    ações = {
        '1': listar_produtos,
        '2': buscar_por_id,
        '3': cadastrar_produto,
        '4': atualizar_produto,
        '5': deletar_produto,
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
        ação = ações.get(escolha)
        if ação:
            ação()
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    menu()
