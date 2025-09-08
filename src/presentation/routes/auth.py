from litestar import Router, get, Controller, Request

from src.presentation.middlewares.auth import AuthenticationMiddleware


class AuthRoutes(Controller):
    path = "/"

    @get(path="data")
    async def auth_data(self, request: Request) -> dict:
        user = request.user
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
