from litestar import get, MediaType
from asyncpg import Connection


@get(path="/sample", media_type=MediaType.JSON, cache=4)
async def sample_route(db_connection: Connection) -> dict[str, str]:
    user = await db_connection.fetchrow('select name from users limit 1')
    return dict(user)
