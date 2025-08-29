from litestar import Controller, post, Request
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from src.core.di import container
from src.domain.entities.common import User, Session
from src.presentation.schemas.user_schema import UserCreateSchema, UserLoginSchema, TokenSchema


class UserController(Controller):
    path = "/users"

    @post("/register")
    async def create_user(self, data: UserCreateSchema) -> bool:
        try:
            user_use_case = container.user_use_case()
            # Usando o método to_entity do schema para criar a entidade
            user = data.to_entity()
            return await user_use_case.register(user)
        except ValueError as e:
            raise HTTPException(detail=str(e), status_code=HTTP_400_BAD_REQUEST)

    @post("/auth")
    async def auth_user(self, data: UserLoginSchema, request: Request) -> TokenSchema:
        try:
            user_use_case = container.user_use_case()
            user_agent = request.headers.get('user-agent')
            ip = request.client.host
            
            token = await user_use_case.authenticate(
                email=data.email,
                password=data.password,
                user_agent=user_agent,
                ip=ip
            )
            
            if not token:
                raise ValueError('Falha na autenticação')
                
            return TokenSchema(token=token)
        except ValueError as e:
            raise HTTPException(detail=str(e), status_code=HTTP_400_BAD_REQUEST)