from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
    """Handler genérico para HTTPException.

    Retorna payload JSON padronizado.
    """
    return Response(
        content={
            "error": "erro de aplicação",
            "path": request.url.path,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        status_code=exc.status_code,
    )


def internal_server_error_handler(_: Request, exc: Exception) -> Response:
    """Handler para erros não tratados (500)."""
    return Response(media_type=MediaType.TEXT, content=str(exc), status_code=500)
