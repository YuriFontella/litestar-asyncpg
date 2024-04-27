from litestar import Router, get
from asyncpg import Connection


@get(path='/', cache=4)
async def sample_route(db_connection: Connection) -> dict[str, str]:
    user = await db_connection.fetchrow('select name from users limit 1')
    if user:
        return dict(user)


router = Router(path='/sample', route_handlers=[sample_route])