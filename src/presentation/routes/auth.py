from litestar import Router, get, Controller
from litestar.types import Scope

from src.presentation.middlewares.auth import AuthenticationMiddleware


class AuthRoutes(Controller):
    path = "/"

    @get(path="data")
    async def auth_data(self, scope: Scope) -> dict:
        user = scope.get("user")
        response = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "status": user["status"],
            "role": user["role"],
        }
        return response


router = Router(
    path="/auth", route_handlers=[AuthRoutes], middleware=[AuthenticationMiddleware]
)
