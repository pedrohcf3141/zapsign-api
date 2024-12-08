# ZapSign API
# Descrição

Este projeto é uma API para o gerenciamento de empresas, documentos e signatários, desenvolvida com Django e Django REST Framework (DRF). A aplicação inclui um backend configurado com Docker Compose para facilitar o desenvolvimento e a execução.

# Tecnologias Utilizadas
Django: Framework para desenvolvimento web.
Django REST Framework (DRF): Para construir APIs RESTful.
PostgreSQL: Banco de dados relacional.
Docker Compose: Para gerenciar os serviços de contêineres.
pytest: Framework para testes em Python.
drf-yasg: Para geração de documentação Swagger e ReDoc da API.
Estrutura do Projeto
O projeto inclui os seguintes serviços configurados em um arquivo docker-compose.yml:

web: Serviço principal que executa a aplicação Django.
db: Serviço do banco de dados PostgreSQL.

# Configuração do Ambiente
# Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto com as variáveis de ambiente necessárias. Para começar, você pode copiar o arquivo env-sample para .env com o seguinte comando:
```bash
Copy code
cp env-sample .env
```
# Instalação e Execução

Construa e inicie os containers:
```bash
Copy code
docker-compose up --build
```

# Acesse a API:

A aplicação estará disponível em http://localhost:8000.


# Executando Testes

Testes com pytest
Para executar os testes, use o seguinte comando:

```bash
Copy code
docker-compose exec web pytest
```

# Testes com Cobertura
Para executar os testes com cobertura, use o pytest-cov:

```bash
Copy code
docker-compose exec web pytest --cov=app
```

O parâmetro --cov=app irá medir a cobertura do código dentro do diretório app.

# Documentação da API
A API inclui documentação interativa acessível nos seguintes endpoints:

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/