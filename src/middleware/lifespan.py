from litestar import Litestar
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: Litestar):
    print('hi')
    yield
    print('bye')
