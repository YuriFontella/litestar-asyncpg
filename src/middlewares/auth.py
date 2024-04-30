from jwt import PyJWTError, decode

from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection

from settings import key
from config.plugin.asyncpg import config


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        try:
            token = connection.headers.get('x-access-token')
            if not token:
                raise NotAuthorizedException()

            auth = decode(jwt=token, key=key, algorithms=["HS256"])
            user = auth.get('id')

            # pool = config.provide_pool(connection.state)
            # async with pool.acquire() as conn:
            #     user = await conn.fetchrow('select name, email from users where id = $1', user)

            if not user:
                raise NotAuthorizedException()

        except PyJWTError:
            raise NotAuthorizedException()

        else:
            return AuthenticationResult(user=user, auth=auth)
