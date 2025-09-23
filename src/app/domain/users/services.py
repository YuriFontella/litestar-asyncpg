from __future__ import annotations

import hashlib
import secrets
import bcrypt
import jwt

from typing import Optional
from dataclasses import dataclass, field
from asyncpg import Connection

from src.app.config.base import get_settings, Settings
from src.app.domain.users.repositories.user import UserRepository
from src.app.domain.users.repositories.session import SessionRepository
from src.app.domain.users.schemas import Token, UserCreate, UserLogin, User


@dataclass
class UsersService:
    """Service layer for user operations using AsyncPG repositories.

    Main responsibilities:
    - Orchestrate user creation and authentication.
    - Generate and validate sessions (persisted in database) + transport JWT.
    - Apply password hashing (bcrypt) and session token derivation (PBKDF2-HMAC).
    - Encapsulate business rules avoiding logic leakage to controllers.
    """

    connection: Connection
    user_repository: UserRepository = field(init=False)
    session_repository: SessionRepository = field(init=False)
    settings: Settings = field(init=False)

    def __post_init__(self) -> None:
        self.user_repository = UserRepository(self.connection)
        self.session_repository = SessionRepository(self.connection)
        self.settings = get_settings()

    async def get_by_email(self, email: str) -> Optional[dict]:
        """Gets user by email."""
        return await self.user_repository.get_by_email(email)

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """Gets user by ID."""
        return await self.user_repository.get_by_id(user_id)

    async def email_exists(self, email: str) -> bool:
        """Checks if email is already registered."""
        return await self.user_repository.email_exists(email)

    async def create(self, data: UserCreate) -> dict:
        """Creates new user with hashed password.

        Security notes:
        - bcrypt.gensalt(10): cost factor 10 (can increase in production if performance allows).
        - Password should never be stored in plain text.
        """
        # Hash password (bcrypt includes internal salt)
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(12)
        )

        # Build domain object with hashed password
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
        """Authenticates user and creates persisted session.

        Summary flow:
        1. Find active user by email.
        2. Validate password via bcrypt.
        3. Generate random token (not stored in plain text) -> derived with PBKDF2-HMAC.
        4. Persist token hash (access_token) in sessions table.
        5. Return JWT containing id + simple token (not derived) that will be re-hashed in middleware.
        """
        # Find active user
        user_record = await self.user_repository.get_by_email(data.email)
        if not user_record or not user_record.get("status", False):
            raise ValueError("No user found")

        # Verify password (secure comparison via bcrypt)
        stored_password = user_record["password"].encode("utf-8")
        if not bcrypt.checkpw(data.password.encode("utf-8"), stored_password):
            raise ValueError("Password is incorrect")

        # Generate session data
        salt = self.settings.app.SESSION_SALT
        random_token = secrets.token_hex()
        user_id = user_record["id"]

        # Derive resistant hash for session token (PBKDF2: increases brute force cost)
        access_token_hash = hashlib.pbkdf2_hmac(
            "sha256", random_token.encode(), salt.encode(), 1000
        )

        # Persist session (don't store original random_token in database)
        session = await self.session_repository.create(
            access_token=access_token_hash.hex(),
            user_agent=user_agent,
            ip=ip,
            user_id=user_id,
        )

        if not session:
            raise ValueError("Something went wrong creating the session")

        # Generate transport JWT with raw token (will be re-hashed in authentication middleware)
        token = jwt.encode(
            {"id": user_id, "access_token": random_token},
            key=self.settings.app.SECRET_KEY,
            algorithm=self.settings.app.JWT_ALGORITHM,
        )

        return Token(token=token)

    async def revoke_session(self, session_id: int) -> bool:
        """Revokes a specific session."""
        return await self.session_repository.revoke(session_id)

    async def revoke_all_sessions(self, user_id: int) -> bool:
        """Revokes all active sessions for the user."""
        return await self.session_repository.revoke_by_user(user_id)

    async def verify_session(self, access_token: str) -> Optional[dict]:
        """Verifies session by access token (hash)."""
        return await self.session_repository.get_by_token(access_token)
