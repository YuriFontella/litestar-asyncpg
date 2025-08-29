from litestar import Controller, get


class RootController(Controller):
    path = "/"

    @get()
    async def root(self) -> dict:
        return {"message": "API is running"}