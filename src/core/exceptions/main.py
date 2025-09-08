from litestar import Request, Response, MediaType
from litestar.exceptions import HTTPException
from src.domain.exceptions import DomainError
from src.core.logging.config import get_logger

logger = get_logger(__name__)


def app_exception_handler(request: Request, exc: HTTPException) -> Response:
    logger.warning(
        "http_exception",
        path=str(request.url.path),
        method=getattr(request, "method", None),
        status_code=exc.status_code,
        error=exc.__class__.__name__,
        detail=exc.detail,
        client=getattr(getattr(request, "client", None), "host", None),
    )
    return Response(
        content={
            "error": "server error",
            "path": request.url.path,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        status_code=exc.status_code,
    )


def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    # Log full details with stack trace but avoid leaking to client
    logger.error(
        "internal_server_error",
        path=str(request.url.path),
        method=getattr(request, "method", None),
        error=exc.__class__.__name__,
        message=str(exc),
        exc_info=True,
    )
    return Response(
        media_type=MediaType.JSON,
        content={"error": "internal_error", "detail": "An unexpected error occurred."},
        status_code=500,
    )


def domain_exception_handler(request: Request, exc: DomainError) -> Response:
    logger.warning(
        "domain_exception",
        path=str(request.url.path),
        method=getattr(request, "method", None),
        error=exc.__class__.__name__,
        detail=str(exc) or exc.__class__.__name__,
        status_code=getattr(exc, "status_code", 400),
    )
    return Response(
        content={
            "error": exc.__class__.__name__,
            "path": request.url.path,
            "detail": str(exc) or exc.__class__.__name__,
            "status_code": getattr(exc, "status_code", 400),
        },
        status_code=getattr(exc, "status_code", 400),
    )
