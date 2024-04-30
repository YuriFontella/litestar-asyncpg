import msgspec
import bcrypt
import jwt

from litestar import Router, post
from litestar.exceptions import HTTPException
from asyncpg import Connection

from settings import key
from src.structs.main import User, Token


@post(path='/register')
async def create_user(data: User, db_connection: Connection) -> bool:
    user = msgspec.to_builtins(data)
    print(user)
    print(msgspec.convert(user, type=User))

    query = """
        select email
        from users
        where email = $1
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


@post(path='/auth')
async def auth_user(data: User, db_connection: Connection) -> Token:
    try:
        query = """
            select * from users
            where email = $1 and status = true
            limit 1
        """
        record = await db_connection.fetchrow(query, data.email)
        if record:
            checkpw = record['password'].encode('utf-8')
            if not bcrypt.checkpw(data.password.encode('utf-8'), checkpw):
                raise Exception('A senha está incorreta')

        else:
            raise Exception('Nenhum usuário encontrado')

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    else:
        token = jwt.encode({'id': record['id']}, key=key, algorithm='HS256')
        return Token(token=token)


router = Router(path='/users', route_handlers=[create_user, auth_user])
