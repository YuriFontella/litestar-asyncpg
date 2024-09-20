import msgspec
import bcrypt
import jwt
import secrets
import hashlib

from litestar import Router, Request, post
from litestar.channels import ChannelsPlugin
from litestar.exceptions import HTTPException
from asyncpg import Connection

from settings import key
from src.structs.main import User, Token


@post(path='/register')
async def create_user(data: User, db_connection: Connection, channels: ChannelsPlugin) -> bool:
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
        insert into users (name, email, password) values ($1, $2, $3) returning id
    """
    user = await db_connection.execute(
        query,
        data.name,
        data.email,
        password.decode('utf-8')
    )

    if user:
        channels.publish('Usuário criado com sucesso!', channels=['notifications'])

    return True


@post(path='/auth')
async def auth_user(data: User, request: Request, db_connection: Connection) -> Token:
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
        salt = 'xYzDeV@0000'
        random = secrets.token_hex()

        user_agent = request.headers.get('user-agent')
        ip = request.client.host
        user_id = record['id']
        access_token = hashlib.pbkdf2_hmac('sha256', random.encode(), salt.encode(), 1000)

        query = """
            insert into sessions (access_token, user_agent, ip, user_id) values ($1, $2, $3, $4) returning id
        """
        session = await db_connection.execute(
            query,
            access_token.hex(),
            user_agent,
            ip,
            user_id
        )

        if session:
            token = jwt.encode({'id': record['id'], 'access_token': random}, key=key, algorithm='HS256')
            return Token(token=token)
        else:
            raise Exception('Algo deu errado')


router = Router(path='/users', route_handlers=[create_user, auth_user])
