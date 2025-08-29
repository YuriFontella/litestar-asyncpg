import bcrypt
import jwt
import secrets
import hashlib
from typing import Optional

from src.domain.entities.common import User, Session
from src.domain.interfaces.repositories import UserRepositoryInterface, SessionRepositoryInterface
from src.application.interfaces.use_cases import UserUseCaseInterface
from settings import key


class UserUseCase(UserUseCaseInterface):
    def __init__(self, user_repository: UserRepositoryInterface, session_repository: SessionRepositoryInterface):
        self.user_repository = user_repository
        self.session_repository = session_repository

    async def register(self, user: User) -> bool:
        existing_user = await self.user_repository.get_by_email(user.email)
        if existing_user:
            raise ValueError('Já existe um cadastro com esse e-mail')

        user_id = await self.user_repository.create(user)
        return bool(user_id)

    async def authenticate(self, email: str, password: str, user_agent: str, ip: str) -> Optional[str]:
        user = await self.user_repository.get_by_email(email)
        if not user or not user.status:
            raise ValueError('Nenhum usuário encontrado')

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError('A senha está incorreta')

        # Gerar token de acesso
        salt = 'xYzDeV@0000'
        random = secrets.token_hex()
        access_token = hashlib.pbkdf2_hmac('sha256', random.encode(), salt.encode(), 1000)

        # Criar sessão
        session = Session(
            access_token=access_token.hex(),
            user_agent=user_agent,
            ip=ip,
            user_id=user.id
        )

        session_id = await self.session_repository.create(session)
        if not session_id:
            raise ValueError('Algo deu errado')

        # Gerar JWT
        token = jwt.encode({'id': user.id, 'access_token': random}, key=key, algorithm='HS256')
        return token

    async def get_user_data(self, user_id: int) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)