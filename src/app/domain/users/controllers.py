from __future__ import annotations

import msgspec
from litestar import Controller, Request, post, get
from litestar.di import Provide
from litestar.channels import ChannelsPlugin
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_201_CREATED

from src.app.domain.users.schemas import Token, UserCreate, UserLogin, UserRead
from src.app.domain.users import urls
from src.app.domain.users.deps import provide_users_service
from src.app.domain.users.services import UsersService


class UserController(Controller):
    """User controller with CRUD operations."""

    path = "/users"
    tags = ["Users"]
    dependencies = {
        "users_service": Provide(provide_users_service, sync_to_thread=False)
    }

    @post(path=urls.USERS_REGISTER, status_code=HTTP_201_CREATED)
    async def create_user(
        self, data: UserCreate, channels: ChannelsPlugin, users_service: UsersService
    ) -> UserRead:
        """Create a new user account."""
        # Validate data
        payload = msgspec.to_builtins(data)
        validated_data = msgspec.convert(payload, type=UserCreate)

        # Check if email already exists
        if await users_service.email_exists(validated_data.email):
            raise HTTPException(
                detail="Já existe um cadastro com esse e-mail", status_code=400
            )

        # Create user
        user_record = await users_service.create(validated_data)
        if user_record:
            channels.publish("Usuário criado com sucesso!", channels=["notifications"])

        return UserRead(
            id=user_record["id"],
            name=user_record["name"],
            email=user_record["email"],
            role=user_record["role"],
            status=user_record["status"],
        )

    @post(path=urls.USERS_AUTH)
    async def authenticate_user(
        self, data: UserLogin, request: Request, users_service: UsersService
    ) -> Token:
        """Authenticate user and return JWT token."""
        try:
            user_agent = request.headers.get("user-agent")
            ip = request.client.host if request.client else None
            return await users_service.authenticate(data, user_agent=user_agent, ip=ip)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @get(path="/{user_id:int}")
    async def get_user(self, user_id: int, users_service: UsersService) -> UserRead:
        """Get user by ID."""
        user_record = await users_service.get_by_id(user_id)
        if not user_record:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return UserRead(
            id=user_record["id"],
            name=user_record["name"],
            email=user_record["email"],
            role=user_record["role"],
            status=user_record["status"],
        )
