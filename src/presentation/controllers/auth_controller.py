from litestar import Controller, get
from litestar.types import Scope

from src.presentation.schemas.user_schema import UserResponseSchema
from src.presentation.middlewares.auth_middleware import auth_required
from src.domain.entities.common import User


class AuthController(Controller):
    path = "/auth"
    guards = [auth_required]

    @get("/data")
    async def auth_data(self, scope: Scope) -> UserResponseSchema:
        user_data = scope.get('user')
        
        # Criando uma entidade User a partir dos dados do escopo
        user = User(
            id=user_data['id'],
            name=user_data['name'],
            email=user_data['email'],
            status=user_data['status'],
            role=user_data['role'],
            password=""  # Campo obrigatório, mas não usado aqui
        )
        
        # Usando o método from_entity para criar o schema de resposta
        return UserResponseSchema.from_entity(user)