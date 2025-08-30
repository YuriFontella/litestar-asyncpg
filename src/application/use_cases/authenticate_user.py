from __future__ import annotations

from dataclasses import dataclass
import hashlib
import secrets
import jwt
import bcrypt
from asyncpg import Connection
from litestar.exceptions import HTTPException

from src.core.config.settings import settings
from src.domain.entities.user import AuthCredentials
from src.domain.entities.token import Token
from src.domain.interfaces.user_repository import UserRepository
from src.domain.interfaces.session_repository import SessionRepository


@dataclass(slots=True)
class AuthenticateUserUseCase:
    user_repo: UserRepository
    session_repo: SessionRepository

    async def execute(
        self,
        conn: Connection,
        creds: AuthCredentials,
        user_agent: str | None,
        ip: str | None,
    ) -> Token:
        record = await self.user_repo.find_active_by_email(conn, creds.email)
        if not record:
            raise HTTPException(status_code=400, detail="Nenhum usuário encontrado")

        checkpw = record.password.encode("utf-8")
        if not bcrypt.checkpw(creds.password.encode("utf-8"), checkpw):
            raise HTTPException(status_code=400, detail="A senha está incorreta")

        salt = settings.access_token_salt
        random = secrets.token_hex()
        access_token_bytes = hashlib.pbkdf2_hmac(
            "sha256", random.encode(), salt.encode(), 1000
        )

        session_id = await self.session_repo.create_session(
            conn=conn,
            access_token=access_token_bytes.hex(),
            user_agent=user_agent,
            ip=ip,
            user_id=int(record.id or 0),
        )

        if not session_id:
            raise HTTPException(status_code=400, detail="Algo deu errado")

        token = jwt.encode(
            {"id": record.id, "access_token": random},
            key=settings.key,
            algorithm=settings.jwt_alg,
        )
        return Token(token=token)
