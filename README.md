# CaixaLivre

O CaixaLivre é uma API simples de gerenciamento de controle de caixa, oferecendo opções para cadastro de vendas, produtos, vendedores, clientes e commissionamento.

## Instalação

1 - O primeiro comando necessário é a instalação das dependências necessárias:

```bash
pip install -r requirements.txt
```

2 - Após a instalação das dependências, é necessário aplicar as migrações. Isso é possível com o comando:

```bash
python manage.py migrate
```

3 - Com as tabelas criadas, é possível iniciar a aplicação com o comando:

```bash
python manage.py runserver 8000
```

Assim a aplicação estará disponível em [localhost:8000](http:localhost:8000)

4 - Há um comando opcional para popular o banco com itens genéricos e ser possível testar algumas funcionalidades da aplicação sem que seja necessário nenhum cadastro manual através do comando:

```bash
python manage.py populate_database
```