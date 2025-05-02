# Documentação da Aplicação: Gerenciador de Produtos

## 1. Visão Geral
Esta aplicação é um sistema de gerenciamento de produtos simples desenvolvido em **Python**, com persistência em **SQLite3**, operações em linha de comando (CLI), suporte a **logs automáticos** e preparada para execução via **Docker**. O usuário pode cadastrar, listar, buscar, atualizar e deletar produtos armazenados localmente.

## 2. Linguagem Escolhida
- Python 3.11
- Gerenciamento de dependências com `pip`
- Docker (imagem baseada em `python:3.11-slim`)

## 3. Recursos e Estrutura da Tabela
A aplicação utiliza um banco SQLite local com a tabela `produtos`:

| Campo          | Tipo de Dado | Obrigatório | Descrição                       |
|----------------|--------------|--------------|----------------------------------|
| `id`           | INTEGER      | Sim (auto)   | Identificador único             |
| `nome`         | TEXT         | Sim          | Nome do produto                  |
| `preco`        | REAL         | Sim          | Preço em R$                     |
| `data_validade`| TEXT         | Não         | Data no formato `DD-MM-AAAA`     |
| `descricao`    | TEXT         | Não         | Texto livre                      |

## 4. Dependências Necessárias

1. Python 3.11 ou superior
2. Pip
3. Docker (opcional)

### Instalação via pip

```bash
pip install -r requirements.txt
```

### Requisitos no `requirements.txt`:
```
colorama==0.4.6
iniconfig==2.1.0
packaging==25.0
pluggy==1.5.0
pytest==8.3.5
```

## 5. Como Executar a Aplicação

### Usando Python diretamente:
```bash
python app.py
```

### Usando Docker:
```bash
docker build -t app-produtos .
docker run -it app-produtos
```

### Para persistir dados locais (Windows):
```bash
docker run -it -v %cd%:/app app-produtos
```

## 6. Funcionalidades

### Menu principal:
```
=== MENU ===
1. Listar produtos
2. Buscar por ID
3. Cadastrar novo
4. Atualizar existente
5. Deletar
6. Sair
```

### Exemplo de uso - Cadastro:
```
Nome: Caneta
Preço: 2.5
Validade: 12-12-2026
Descrição: Azul
Produto cadastrado com sucesso!
```

### Exemplo - Busca por ID:
```
ID do produto (ou 'sair'): 1
=== Produto Encontrado ===
ID: 1
Nome: Caneta
...
```

## 7. Logs
Logs automáticos são registrados no arquivo `app.log`, que é gerado na **raiz do projeto** por padrão.

Se estiver rodando dentro de um contêiner Docker, o arquivo também será criado dentro do contêiner. Para acessá-lo, você pode:

- Mapear um volume com `-v %cd%:/app` (Windows) ou `-v $(pwd):/app` (Linux/macOS)
- Ou copiar do contêiner manualmente com:
```bash
docker cp <nome-do-container>:/app/app.log ./app.log
```

### Exemplo de conteúdo do log:
```
2024-05-01 22:10:34 - INFO - Produto cadastrado: nome=Caneta, preco=2.5
2024-05-01 22:12:55 - WARNING - Produto não encontrado (id=99)
2024-05-01 22:13:10 - INFO - Produto deletado (id=1)
```

## 8. Testes

### Requisitos:
Antes de executar os testes, certifique-se de:
- Estar na raiz do projeto (`dti_app_produtos`)
- Ter o Python e o `pytest` instalados

### Passos:

1. (Opcional) Crie e ative um ambiente virtual:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Defina o PYTHONPATH para garantir que os testes encontrem os módulos:

**Windows (PowerShell):**
```bash
$env:PYTHONPATH = "."
```

**Linux/macOS:**
```bash
export PYTHONPATH=.
```

4. Execute os testes:
```bash
pytest -q
```

Os testes cobrem funcionalidades de CRUD, validações e formatação de dados. Certifique-se de que as pastas `tests/`, `domain/` e `persistence/` contêm arquivos `__init__.py`.

## 9. Considerações Finais

- A aplicação é simples, testada com pytest, e pode ser executada em qualquer ambiente com Docker ou Python instalado.
- O sistema previne operações quando o banco está vazio.
- Todos os dados são registrados em logs automáticos para auditoria e depuração.
