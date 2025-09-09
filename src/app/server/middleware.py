from __future__ import annotations

from litestar.types import ASGIApp, Receive, Scope, Send


def factory(app: ASGIApp) -> ASGIApp:
    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        await app(scope, receive, send)

    return middleware
