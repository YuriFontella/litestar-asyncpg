from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import bcrypt

from src.domain.entities.user import User
from src.domain.interfaces.user_repository import UserRepository
from src.domain.exceptions import UserAlreadyExists


@dataclass(slots=True)
class RegisterUserUseCase:
    user_repo: UserRepository

    async def execute(self, conn: Any, data: User) -> bool:
        exists = await self.user_repo.find_by_email(conn, data.email)
        if exists:
            raise UserAlreadyExists("Já existe um cadastro com esse e-mail")

        hashed = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt(10))
        user = User(name=data.name, email=data.email, password=hashed.decode("utf-8"))
        user_id = await self.user_repo.create(conn, user)
        return bool(user_id)
