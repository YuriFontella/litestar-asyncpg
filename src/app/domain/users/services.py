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
from src.app.domain.users.schemas import Token, UserCreate, UserLogin


@dataclass
class UsersService:
    """Camada de serviço para operações de usuário usando repositórios AsyncPG.

    Responsabilidades principais:
    - Orquestrar criação e autenticação de usuários.
    - Gerar e validar sessões (persistidas no banco) + JWT de transporte.
    - Aplicar hashing de senhas (bcrypt) e derivação de token de sessão (PBKDF2-HMAC).
    - Encapsular regras de negócio evitando vazamento de lógica para controllers.
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
        """Obtém usuário pelo e-mail."""
        return await self.user_repository.get_by_email(email)

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """Obtém usuário pelo ID."""
        return await self.user_repository.get_by_id(user_id)

    async def email_exists(self, email: str) -> bool:
        """Verifica se e-mail já está cadastrado."""
        return await self.user_repository.email_exists(email)

    async def create(self, data: UserCreate) -> dict:
        """Cria novo usuário com senha hasheada.

        Notas de segurança:
        - bcrypt.gensalt(10): fator de custo 10 (pode aumentar em produção se performance permitir).
        - Senha nunca deve ser armazenada em texto claro.
        """
        # Hash password (bcrypt includes internal salt)
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"), bcrypt.gensalt(10)
        )

        # Monta objeto de domínio com senha hasheada
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
        """Autentica usuário e cria sessão persistida.

        Fluxo resumido:
        1. Busca usuário ativo por e-mail.
        2. Valida senha via bcrypt.
        3. Gera token aleatório (não armazenado em claro) -> derivado com PBKDF2-HMAC.
        4. Persiste hash do token (access_token) na tabela de sessões.
        5. Retorna JWT contendo id + token simples (não derivado) que será re-hasheado no middleware.
        """
        # Busca usuário ativo
        user_record = await self.user_repository.get_by_email(data.email)
        if not user_record or not user_record.get("status", False):
            raise ValueError("Nenhum usuário encontrado")

        # Verifica senha (comparação segura via bcrypt)
        stored_password = user_record["password"].encode("utf-8")
        if not bcrypt.checkpw(data.password.encode("utf-8"), stored_password):
            raise ValueError("A senha está incorreta")

        # Gera dados da sessão
        salt = self.settings.app.SESSION_SALT
        random_token = secrets.token_hex()
        user_id = user_record["id"]

        # Deriva hash resistente para token de sessão (PBKDF2: aumenta custo de brute force)
        access_token_hash = hashlib.pbkdf2_hmac(
            "sha256", random_token.encode(), salt.encode(), 1000
        )

        # Persiste sessão (não guardar random_token original no banco)
        session = await self.session_repository.create(
            access_token=access_token_hash.hex(),
            user_agent=user_agent,
            ip=ip,
            user_id=user_id,
        )

        if not session:
            raise ValueError("Algo deu errado ao criar a sessão")

        # Gera JWT de transporte com token bruto (será re-hasheado no middleware de autenticação)
        token = jwt.encode(
            {"id": user_id, "access_token": random_token},
            key=self.settings.app.SECRET_KEY,
            algorithm=self.settings.app.JWT_ALGORITHM,
        )

        return Token(token=token)

    async def revoke_session(self, session_id: int) -> bool:
        """Revoga uma sessão específica."""
        return await self.session_repository.revoke(session_id)

    async def revoke_all_sessions(self, user_id: int) -> bool:
        """Revoga todas as sessões ativas do usuário."""
        return await self.session_repository.revoke_by_user(user_id)

    async def verify_session(self, access_token: str) -> Optional[dict]:
        """Verifica sessão pelo access token (hash)."""
        return await self.session_repository.get_by_token(access_token)
