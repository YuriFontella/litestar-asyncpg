from __future__ import annotations

import hashlib
import secrets
from typing import Optional
from dataclasses import dataclass, field

import bcrypt
import jwt
from asyncpg import Connection

from src.app.config.base import get_settings, Settings
from src.app.config.constants import SESSION_SALT
from src.app.domain.users.repositories.user import UserRepository
from src.app.domain.users.repositories.session import SessionRepository
from src.app.domain.users.schemas import Token, UserCreate, UserLogin


@dataclass
class UsersService:
    """Service layer for user-related operations using AsyncPG repositories."""

    connection: Connection
    user_repository: UserRepository = field(init=False)
    session_repository: SessionRepository = field(init=False)
    settings: Settings = field(init=False)

    def __post_init__(self) -> None:
        self.user_repository = UserRepository(self.connection)
        self.session_repository = SessionRepository(self.connection)
        self.settings = get_settings()

    async def get_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        return await self.user_repository.get_by_email(email)

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID."""
        return await self.user_repository.get_by_id(user_id)

    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return await self.user_repository.email_exists(email)

    async def create(self, data: UserCreate) -> dict:
        """Create a new user with hashed password."""
        # Hash the password
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(10)
        )

        # Create user data with hashed password
        from src.app.domain.users.schemas import User

        user_data = User(
            name=data.name,
            email=data.email,
            password=hashed_password.decode("utf-8"),
            role=data.role,
        )

        return await self.user_repository.create(user_data)

    async def authenticate(
        self, data: UserLogin, user_agent: str | None, ip: str | None
    ) -> Token:
        """Authenticate user and create session."""
        # Get user by email with active status
        user_record = await self.user_repository.get_by_email(data.email)
        if not user_record or not user_record.get("status", False):
            raise ValueError("Nenhum usuário encontrado")

        # Verify password
        stored_password = user_record["password"].encode("utf-8")
        if not bcrypt.checkpw(data.password.encode("utf-8"), stored_password):
            raise ValueError("A senha está incorreta")

        # Generate session data
        salt = SESSION_SALT
        random_token = secrets.token_hex()
        user_id = user_record["id"]

        # Create access token hash
        access_token_hash = hashlib.pbkdf2_hmac(
            "sha256", random_token.encode(), salt.encode(), 1000
        )

        # Create session
        session = await self.session_repository.create(
            access_token=access_token_hash.hex(),
            user_agent=user_agent,
            ip=ip,
            user_id=user_id,
        )

        if not session:
            raise ValueError("Algo deu errado ao criar a sessão")

        # Generate JWT token
        token = jwt.encode(
            {"id": user_id, "access_token": random_token},
            key=self.settings.app.SECRET_KEY,
            algorithm=self.settings.app.JWT_ENCRYPTION_ALGORITHM,
        )

        return Token(token=token)

    async def revoke_session(self, session_id: int) -> bool:
        """Revoke a user session."""
        return await self.session_repository.revoke(session_id)

    async def revoke_all_sessions(self, user_id: int) -> bool:
        """Revoke all sessions for a user."""
        return await self.session_repository.revoke_by_user(user_id)

    async def verify_session(self, access_token: str) -> Optional[dict]:
        """Verify session by access token."""
        return await self.session_repository.get_by_token(access_token)
