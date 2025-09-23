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

### 1. Prerequisites

* Python 3.13+
* [Poetry](https://python-poetry.org/) (dependency manager)

Poetry installation (if you don't have it):

```bash
curl -sSL https://install.python-poetry.org | python3 -
# then make sure poetry is in PATH according to printed instructions
```

### 2. Environment variables (.env)

Copy the `.env.example` file to `.env` and change the values as needed:

```bash
cp .env.example .env
```

### 3. Install dependencies

```bash
poetry install
```

Configure pre-commit hooks:

```bash
pre-commit install --config pre-commit.yaml
```

Optional: activate virtual shell

```bash
poetry shell
```

### 4. Database

Create the database (adjust the name according to your DSN):

```bash
createdb db
```

If necessary apply manual SQL migrations (e.g.: content in `src/app/db/migrations/`).

### 5. Run the server

The `app` script defined in `pyproject.toml` wraps the Litestar CLI.

Basic command:

```bash
poetry run app run
```

Examples with options:

```bash
poetry run app run -r -P -d -p 9000 -H 0.0.0.0
poetry run app run --wc 4
poetry run app run -h
```

(Same as using `litestar run` directly, but ensuring the environment configured by the script.)

### 6. OpenAPI / ReDoc

Access at:

```
http://localhost:PORT/schema/redoc
```

Replace `PORT` with the port used (default 8000 if not specified).
