import hashlib

from jwt import PyJWTError, decode

from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection

from src.core.config.settings import settings
from src.infrastructure.database.asyncpg import config


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        try:
            token = connection.headers.get("x-access-token")
            if not token:
                raise NotAuthorizedException()

            auth = decode(jwt=token, key=settings.key, algorithms=[settings.jwt_alg])
            salt = settings.access_token_salt
            access_token = hashlib.pbkdf2_hmac(
                "sha256", auth["access_token"].encode(), salt.encode(), 1000
            )
            user_id = auth.get("id")

            pool = config.provide_pool(connection.scope["app"].state)
            async with pool.acquire() as conn:
                query = """
                    select u.id, u.name, u.email, u.role, u.status 
                    from users u 
                    join sessions s on u.id = s.user_id
                    where 
                        u.id = $1 and
                        s.access_token = $2 and
                        s.revoked = false and
                        u.status = true
                """
                user = await conn.fetchrow(query, user_id, access_token.hex())

            if not user:
                raise NotAuthorizedException()

        except PyJWTError:
            raise NotAuthorizedException()

        else:
            return AuthenticationResult(user=user, auth=auth)
