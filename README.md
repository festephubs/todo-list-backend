# TODO List Backend

API REST para gerenciamento de tarefas (TODO List) construída com **FastAPI** e **Python 3.12+**.

## Stack

- **FastAPI** - Framework web async de alta performance
- **SQLAlchemy 2.0** - ORM com suporte async
- **Alembic** - Migrations de banco de dados
- **Pydantic v2** - Validação e serialização de dados
- **JWT (python-jose)** - Autenticação via tokens
- **PostgreSQL / SQLite** - Banco de dados

## Arquitetura

```
app/
├── api/              # Camada de apresentação (endpoints)
│   ├── deps.py       # Dependências compartilhadas (auth, db session)
│   └── v1/
│       └── endpoints/
│           ├── auth.py
│           └── todos.py
├── core/             # Configuração e infraestrutura
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/           # Modelos SQLAlchemy (entidades)
│   ├── user.py
│   └── todo.py
├── repositories/     # Camada de acesso a dados
│   ├── user.py
│   └── todo.py
├── schemas/          # Schemas Pydantic (DTOs)
│   ├── auth.py
│   ├── user.py
│   └── todo.py
├── services/         # Camada de regras de negócio
│   ├── auth.py
│   └── todo.py
└── main.py           # Entry point da aplicação
```

## Endpoints

### Auth
| Método | Endpoint              | Descrição            |
|--------|-----------------------|----------------------|
| POST   | `/api/v1/auth/register` | Registro de usuário |
| POST   | `/api/v1/auth/login`    | Login (retorna JWT) |
| GET    | `/api/v1/auth/me`       | Usuário autenticado |

### Todos
| Método | Endpoint                  | Descrição            |
|--------|---------------------------|----------------------|
| POST   | `/api/v1/todos`           | Criar todo           |
| GET    | `/api/v1/todos`           | Listar todos         |
| GET    | `/api/v1/todos/{id}`      | Buscar por ID        |
| PATCH  | `/api/v1/todos/{id}`      | Atualizar todo       |
| DELETE | `/api/v1/todos/{id}`      | Deletar todo         |

## Setup Local

```bash
# Criar virtual environment
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e ".[dev]"

# Copiar variáveis de ambiente
cp .env.example .env

# Rodar servidor de desenvolvimento
fastapi dev app/main.py
```

A documentação interativa estará disponível em: http://localhost:8000/docs

## Docker

```bash
docker compose up --build
```

## Testes

```bash
pytest
```

## Variáveis de Ambiente

| Variável                     | Padrão                              | Descrição                     |
|------------------------------|--------------------------------------|-------------------------------|
| `DATABASE_URL`               | `sqlite+aiosqlite:///./todo.db`     | URL de conexão do banco       |
| `SECRET_KEY`                 | `change-me-in-production`           | Chave secreta para JWT        |
| `ALGORITHM`                  | `HS256`                             | Algoritmo de criptografia JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| `30`                                | Tempo de expiração do token   |
| `CORS_ORIGINS`               | `["http://localhost:4200"]`         | Origens permitidas no CORS    |
