from __future__ import annotations

from litestar.types import ASGIApp, Receive, Scope, Send


def factory(app: ASGIApp) -> ASGIApp:
    """Base middleware factory (placeholder).

    Currently doesn't alter the flow; extension point to add:
    - structured logging
    - metrics
    - tracing
    - header manipulation
    """

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        # Forward directly without changes
        await app(scope, receive, send)

    return middleware
