from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import NoReturn


def setup_environment() -> None:
    """Configure environment and Litestar app path."""
    current_path = Path(__file__).parent.parent.resolve()
    sys.path.append(str(current_path))
    os.environ.setdefault("LITESTAR_APP", "src.app.asgi:create_app")


def run_cli() -> NoReturn:
    """Run Litestar CLI with configured app."""
    setup_environment()
    try:
        from litestar.cli.main import litestar_group

        sys.exit(litestar_group())
    except ImportError as exc:  # pragma: no cover - environment specific
        print(
            "Could not load required libraries. Please check your installation and virtual environment.",
        )
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    run_cli()
