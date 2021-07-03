# CaixaLivre

O CaixaLivre é uma API simples de gerenciamento de controle de caixa, oferecendo opções para cadastro de vendas, produtos, vendedores, clientes e commissionamento.

## Instalação

1 - O primeiro comando necessário é a criação de um virtual environment para a instalação das depêndencias do projeto. Primeiramente criaremos o ambiente virtual com o comando:

```bash
python -m venv <caminho do venv>/caixalivre
```

2 - Após a criação do venv, executaremos um comando para utilizá-lo

```bash
source <caminho do venv>/caixalivre/bin/activate
```

3 - Após a criação da venv é necessário a instalação das dependências necessárias:

```bash
pip install -r requirements.txt
```

4 - Após a instalação das dependências, é necessário aplicar as migrações. Isso é possível com o comando:

```bash
python manage.py migrate
```

5 - Com as tabelas criadas, é possível iniciar a aplicação com o comando:

```bash
python manage.py runserver 8000
```

Assim a aplicação estará disponível em [localhost:8000](http:localhost:8000)

6 - Há um comando opcional para popular o banco com itens genéricos e ser possível testar algumas funcionalidades da aplicação sem que seja necessário nenhum cadastro manual através do comando:

```bash
python manage.py populate_database
```