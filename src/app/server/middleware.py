from __future__ import annotations

from litestar.types import ASGIApp, Receive, Scope, Send


def factory(app: ASGIApp) -> ASGIApp:
    """Factory de middleware base (placeholder).

    Atualmente não altera o fluxo; ponto de extensão para adicionar:
    - logging estruturado
    - métricas
    - tracing
    - manipulação de headers
    """

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        # Encaminha diretamente sem alteração
        await app(scope, receive, send)

    return middleware
