from __future__ import annotations

from dataclasses import dataclass
from asyncpg import Connection

from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.entities.user import User, AuthCredentials
from src.domain.entities.token import Token


@dataclass(slots=True)
class RegisterUserController:
    use_case: RegisterUserUseCase

    async def register(self, conn: Connection, data: User) -> bool:
        return await self.use_case.execute(conn, data)


@dataclass(slots=True)
class AuthenticateUserController:
    use_case: AuthenticateUserUseCase

    async def authenticate(
        self,
        conn: Connection,
        creds: AuthCredentials,
        user_agent: str | None,
        ip: str | None,
    ) -> Token:
        return await self.use_case.execute(conn, creds, user_agent, ip)
