from litestar import Router, get
from litestar.types import Scope

from src.presentation.middlewares.auth import AuthenticationMiddleware


@get(path='/data')
async def auth_data(scope: Scope) -> dict:
    user = scope.get('user')

    response = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'status': user['status'],
        'role': user['role']
    }

    return response


router = Router(
    path='/auth',
    route_handlers=[auth_data],
    middleware=[AuthenticationMiddleware]
)

