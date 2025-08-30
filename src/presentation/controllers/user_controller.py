from __future__ import annotations

from dataclasses import dataclass
from asyncpg import Connection

from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.entities.user import User, AuthCredentials
from src.domain.entities.token import Token


@dataclass(slots=True)
class UserController:
    register_uc: RegisterUserUseCase
    authenticate_uc: AuthenticateUserUseCase

    async def register(self, conn: Connection, data: User) -> bool:
        return await self.register_uc.execute(conn, data)

    async def authenticate(
        self, conn: Connection, creds: AuthCredentials, user_agent: str | None, ip: str | None
    ) -> Token:
        return await self.authenticate_uc.execute(conn, creds, user_agent, ip)

