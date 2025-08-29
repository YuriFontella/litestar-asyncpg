# Litestar Asyncpg Clean Architecture

Este projeto implementa uma API usando Litestar com AsyncPG seguindo os princípios de Clean Architecture.

## Arquitetura

O projeto segue a arquitetura limpa (Clean Architecture) com as seguintes camadas:

- **Domain**: Contém as entidades de negócio e interfaces de repositório
- **Application**: Contém os casos de uso e interfaces de aplicação
- **Infrastructure**: Contém implementações concretas de repositórios e serviços
- **Presentation**: Contém controllers, schemas e rotas da API
- **Core**: Contém configurações, exceções e injeção de dependência

## Tecnologias

- Litestar: Framework web assíncrono
- AsyncPG: Driver PostgreSQL assíncrono
- Dependency Injector: Biblioteca para injeção de dependência
- PyJWT: Biblioteca para autenticação JWT
- BCrypt: Biblioteca para hash de senhas
- Python-dotenv: Biblioteca para carregar variáveis de ambiente

## Funcionalidades

* Roteamento
* Canais (websocket)
* Eventos
* Middlewares (cors, csrf, rate limit)
* Autenticação e Autorização
* Injeção de Dependência
* Arquivos Estáticos

## Configuração

### Arquivo .env

```
KEY=secret
DSN=postgresql://user:password@host:port/db
```

### Instalação de Dependências

```bash
poetry install
```

Ou

```bash
pip install -r requirements.txt
```

### Banco de Dados

```bash
create database db 
```

## Executando o Servidor

```bash
litestar run
```

Opções adicionais:

```bash
litestar run -r -P -d -p 9000 -H 0.0.0.0  # Reload, Production, Debug, Port, Host
```

```bash
litestar run --wc 4  # Workers Count
```

```bash
litestar run -h  # Help
```

## Testes

Execute os testes com:

```bash
./run_tests.sh
```

Ou

```bash
python -m pytest tests/ -v
```

## Documentação da API

Acesse a documentação OpenAPI em:

```
http://localhost:8000/schema/redoc
```