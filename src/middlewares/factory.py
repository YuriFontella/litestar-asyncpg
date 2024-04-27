from litestar.types import ASGIApp, Scope, Receive, Send


def factory(app: ASGIApp) -> ASGIApp:
    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:

        await app(scope, receive, send)

    return middleware
