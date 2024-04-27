from jwt import PyJWTError, decode

from litestar.middleware import AbstractAuthenticationMiddleware, AuthenticationResult
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:
        try:
            token = connection.headers.get('x-access-token')
            if not token:
                raise NotAuthorizedException()

            auth = decode(jwt=token, key='!!$$dev$$00', algorithms=["HS256"])

            user = auth.get('id')
            if not user:
                raise NotAuthorizedException()

        except PyJWTError:
            raise NotAuthorizedException()

        else:
            return AuthenticationResult(user=user, auth=auth)
