from __future__ import annotations

import logging
import sys
from typing import Any, Dict

import structlog
from src.core.config.settings import settings

_ENV = settings.environment
_SERVICE = settings.service_name
_LEVEL_NAME = settings.log_level
_LEVEL = getattr(logging, _LEVEL_NAME, logging.INFO)


def _add_service_and_env(_: Any, __: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    event_dict.setdefault("service", _SERVICE)
    event_dict.setdefault("env", _ENV)
    return event_dict


def setup_logging() -> None:
    """Configure stdlib logging and structlog with sensible defaults.

    - Uses JSON in non-dev environments; pretty console output in dev/local.
    - Honors values from Settings: environment, log_level, service_name.
    """

    # Stdlib logging to stdout with simple message pass-through
    logging.basicConfig(
        level=_LEVEL,
        format="%(message)s",
        stream=sys.stdout,
    )

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    base_processors = [
        structlog.contextvars.merge_contextvars,
        _add_service_and_env,
        structlog.processors.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Renderer selection based on environment
    if _ENV in {"dev", "development", "local"}:
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *base_processors,
            renderer,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:  # type: ignore[name-defined]
    """Return a structlog logger bound with service/env context."""
    return structlog.get_logger(name) if name else structlog.get_logger()
