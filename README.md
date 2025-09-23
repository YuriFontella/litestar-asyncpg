## Litestar Asyncpg Plugin

### Features

* Routing
* Channels (websocket)
* Events
* Middlewares (cors, csrf, rate limit)
* Allowed Hosts
* Stores
* Security / Guards (authentication)
* Caching
* Plugins
* Static Files

## Setup

### 1. Pré‑requisitos

* Python 3.13+
* [Poetry](https://python-poetry.org/) (gerenciador de dependências)

Instalação do Poetry (caso não tenha):

```bash
curl -sSL https://install.python-poetry.org | python3 -
# depois garanta que o poetry esteja no PATH conforme instruções impressas
```

### 2. Variáveis de ambiente (.env)

Copie o arquivo `.env.example` para `.env` e altere os valores conforme necessário:

```bash
cp .env.example .env
```

### 3. Instalar dependências

```bash
poetry install
```

Configure os hooks de pre-commit:

```bash
pre-commit install --config pre-commit.yaml
```

Opcional: ativar o shell virtual

```bash
poetry shell
```

### 4. Banco de dados

Crie o database (ajuste o nome conforme seu DSN):

```bash
createdb db
```

Se necessário aplique migrações SQL manuais (ex.: conteúdo em `src/app/db/migrations/`).

### 5. Executar o servidor

O script `app` definido em `pyproject.toml` encapsula o CLI do Litestar.

Comando básico:

```bash
poetry run app run
```

Exemplos com opções:

```bash
poetry run app run -r -P -d -p 9000 -H 0.0.0.0
poetry run app run --wc 4
poetry run app run -h
```

(O mesmo que usar diretamente `litestar run`, porém garantindo o ambiente configurado pelo script.)

### 6. OpenAPI / ReDoc

Acesse em:

```
http://localhost:PORT/schema/redoc
```

Substitua `PORT` pela porta utilizada (padrão 8000 se não especificado).
