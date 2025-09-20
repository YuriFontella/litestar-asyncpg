from __future__ import annotations

import hashlib

from jwt import PyJWTError, decode

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from src.app.config.base import get_settings
from src.app.config import app as config

settings = get_settings()


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    # Middleware de autenticação baseado em JWT + sessão persistida no banco.
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        try:
            token = connection.headers.get("x-access-token")
            if not token:
                raise NotAuthorizedException()

            auth = decode(
                jwt=token,
                key=settings.app.SECRET_KEY,
                algorithms=[settings.app.JWT_ALGORITHM],
            )
            salt = settings.app.SESSION_SALT
            access_token = hashlib.pbkdf2_hmac(
                "sha256", auth["access_token"].encode(), salt.encode(), 1000
            )
            user_id = auth.get("id")

            # Obtém pool asyncpg via configuração do plugin (evita recriar conexões)
            pool = config.asyncpg.provide_pool(connection.scope["app"].state)
            async with pool.acquire() as conn:
                query = """
                    select u.id, u.name, u.email, u.role, u.status from users u
                    join sessions s on u.id = s.user_id
                    where u.id = $1 and s.access_token = $2 and s.revoked = false and u.status = true
                """
                user = await conn.fetchrow(query, user_id, access_token.hex())

            if not user:
                raise NotAuthorizedException()

        except PyJWTError:
            raise NotAuthorizedException()

        else:
            return AuthenticationResult(user=user, auth=auth)
