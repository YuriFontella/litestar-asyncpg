from litestar import Router, MediaType, get

from src.presentation.controllers.root_controller import RootController


controller = RootController()


@get(path='/', media_type=MediaType.JSON)
async def root() -> bool:
    return await controller.root()


router = Router(path='/root', route_handlers=[root])

