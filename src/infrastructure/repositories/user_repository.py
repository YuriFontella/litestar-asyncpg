from typing import Optional, Any
import bcrypt

from src.domain.entities.common import User, Session
from src.domain.interfaces.repositories import UserRepositoryInterface, SessionRepositoryInterface
from src.infrastructure.database.connection import DatabaseConnection


class UserRepository(UserRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def create(self, user: User) -> int:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(10))
            
            query = """
                insert into users (name, email, password, role, status) 
                values ($1, $2, $3, $4, $5) returning id
            """
            
            result = await conn.fetchval(
                query,
                user.name,
                user.email,
                password.decode('utf-8'),
                user.role,
                user.status
            )
            
            return result

    async def get_by_email(self, email: str) -> Optional[User]:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = """
                select * from users
                where email = $1
                limit 1
            """
            
            record = await conn.fetchrow(query, email)
            
            if record:
                return User(
                    id=record['id'],
                    name=record['name'],
                    email=record['email'],
                    password=record['password'],
                    role=record['role'],
                    status=record['status']
                )
            
            return None

    async def get_by_id(self, user_id: int) -> Optional[User]:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = """
                select * from users
                where id = $1
                limit 1
            """
            
            record = await conn.fetchrow(query, user_id)
            
            if record:
                return User(
                    id=record['id'],
                    name=record['name'],
                    email=record['email'],
                    password=record['password'],
                    role=record['role'],
                    status=record['status']
                )
            
            return None


class SessionRepository(SessionRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def create(self, session: Session) -> int:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = """
                insert into sessions (access_token, user_agent, ip, user_id) 
                values ($1, $2, $3, $4) returning id
            """
            
            result = await conn.fetchval(
                query,
                session.access_token,
                session.user_agent,
                session.ip,
                session.user_id
            )
            
            return result

    async def get_by_token_and_user_id(self, token: str, user_id: int) -> Optional[Session]:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = """
                select * from sessions
                where access_token = $1 and user_id = $2 and revoked = false
                limit 1
            """
            
            record = await conn.fetchrow(query, token, user_id)
            
            if record:
                return Session(
                    id=record['id'],
                    access_token=record['access_token'],
                    user_agent=record['user_agent'],
                    ip=record['ip'],
                    revoked=record['revoked'],
                    user_id=record['user_id'],
                    date=record['date']
                )
            
            return None