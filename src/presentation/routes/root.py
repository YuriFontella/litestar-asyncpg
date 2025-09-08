from litestar import Router, MediaType, Controller, get

from src.presentation.controllers.root_controller import RootController

# Instantiate controller at module level
root_controller = RootController()


class RootRoutes(Controller):
    path = "/"

    @get(path="", media_type=MediaType.JSON)
    async def root(self) -> dict:
        ok = await root_controller.root()
        return {"status": "ok" if ok else "fail"}


router = Router(path="/", route_handlers=[RootRoutes])
