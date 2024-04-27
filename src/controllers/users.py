import msgspec

from litestar import Router, post
from src.structs.main import User


@post(path='/register')
async def create_user(data: User) -> bool:
    user = msgspec.to_builtins(data)
    print(user)
    print(msgspec.convert(user, type=User))

    return True


router = Router(path='/users', route_handlers=[create_user])
