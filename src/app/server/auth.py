from __future__ import annotations

import hashlib

from jwt import PyJWTError, decode

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult

from ..config import settings
from .plugins import asyncpg_config


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:  # type: ignore[override]
        try:
            token = connection.headers.get("x-access-token")
            if not token:
                raise NotAuthorizedException()

            auth = decode(jwt=token, key=settings.key, algorithms=["HS256"])
            salt = "xYzDeV@0000"
            access_token = hashlib.pbkdf2_hmac(
                "sha256", auth["access_token"].encode(), salt.encode(), 1000
            )
            user_id = auth.get("id")

            # get asyncpg pool via plugin config
            pool = asyncpg_config.provide_pool(connection.scope["app"].state)
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
