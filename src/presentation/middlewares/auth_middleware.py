import jwt
from typing import Optional, Callable, Any
from litestar.connection import ASGIConnection
from litestar.middleware import MiddlewareProtocol
from litestar.types import Receive, Scope, Send
from litestar.exceptions import NotAuthorizedException

from src.core.di import container
from src.core.config import settings


class AuthMiddleware(MiddlewareProtocol):
    def __init__(self, app: Callable[[Scope, Receive, Send], Any]) -> None:
        self.app = app
        self.user_use_case = container.user_use_case()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        connection = ASGIConnection(scope, receive, send)
        authorization = connection.headers.get("authorization")

        if not authorization or not authorization.startswith("Bearer "):
            await self.app(scope, receive, send)
            return

        token = authorization.replace("Bearer ", "")

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            access_token = payload.get("access_token")

            if not access_token:
                await self.app(scope, receive, send)
                return

            user_agent = connection.headers.get("user-agent", "")
            client_ip = connection.client.host

            session = await self.user_use_case.get_session_by_token(
                access_token=access_token,
                user_agent=user_agent,
                client_ip=client_ip
            )

            if not session:
                await self.app(scope, receive, send)
                return

            user = await self.user_use_case.get_user_by_id(session.user_id)

            if not user:
                await self.app(scope, receive, send)
                return

            scope["user"] = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            }
            scope["session"] = {
                "id": session.id,
                "user_id": session.user_id,
                "access_token": session.access_token,
                "user_agent": session.user_agent,
                "client_ip": session.client_ip,
                "revoked": session.revoked,
                "created_at": session.created_at,
            }

        except Exception:
            pass

        await self.app(scope, receive, send)


def auth_required(connection: ASGIConnection) -> None:
    if not connection.scope.get("user"):
        raise NotAuthorizedException("Not authenticated")