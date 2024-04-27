from litestar import Router, get
from src.structs.main import User


@get(path='/')
async def create_user() -> User:
    return User(email='yuri@gmail.com', password='123456')


router = Router(path='/users', route_handlers=[create_user])
