from litestar import Router, MediaType, Controller, get

from src.presentation.controllers.root_controller import RootController

# Instantiate controller at module level
root_controller = RootController()


class RootRoutes(Controller):
    path = "/"

    @get(media_type=MediaType.JSON)
    async def root(self) -> bool:
        return await root_controller.root()


router = Router(path="/root", route_handlers=[RootRoutes])
