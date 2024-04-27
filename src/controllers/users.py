import msgspec
import bcrypt

from litestar import Router, post
from litestar.exceptions import HTTPException
from asyncpg import Connection
from src.structs.main import User


@post(path='/register')
async def create_user(data: User, db_connection: Connection) -> bool:
    user = msgspec.to_builtins(data)
    print(user)
    print(msgspec.convert(user, type=User))

    query = """
        SELECT email
        FROM users
        WHERE email = $1
    """
    record = await db_connection.fetchrow(query, data.email)

    if record:
        raise HTTPException(detail='Já existe um cadastro com esse e-mail', status_code=400)

    password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt(10))

    query = """
        insert into users (name, email, password) values ($1, $2, $3)
    """
    await db_connection.execute(
        query,
        data.name,
        data.email,
        password.decode('utf-8')
    )

    return True


router = Router(path='/users', route_handlers=[create_user])
