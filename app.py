from litestar import Litestar

from config.plugin import asyncpg
from src.middleware.factory import middleware_factory
from src.middleware.lifespan import lifespan

from src.controller.players import sample_route

app = Litestar(
    plugins=[asyncpg],
    route_handlers=[sample_route],
    middleware=[middleware_factory],
    lifespan=[lifespan]
)
