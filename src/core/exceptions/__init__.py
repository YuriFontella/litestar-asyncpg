from litestar import Request, Response, MediaType
from litestar.exceptions import HTTPException


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
    return Response(
        content={
            'error': 'server error',
            'path': request.url.path,
            'detail': exc.detail,
            'status_code': exc.status_code,
        },
        status_code=exc.status_code
    )


def internal_server_error_handler(_: Request, exc: Exception) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=500
    )