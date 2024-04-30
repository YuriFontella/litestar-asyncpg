## Litestar Asyncpg Plugin

Usage:

* Routing
* Channels (websocket)
* Events
* Middlewares (cors, csrf, rate limit)
* Stores
* Security / Guards (authentication)
* Caching
* Plugins
* Static Files

## Setup

#### .env

```
KEY=secret
DSN=postgresql://user:password@host:port/db
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Database

```sql
create database db 
```

### Run Server


```bash
litestar run
```

```bash
litestar run -r -P -d -p 9000 -H 0.0.0.0
```
```bash
litestar run --wc 4
```
```bash
litestar run -h
```

### OpenAPI

```bash
localhost:port/schema/redoc
```