from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RootController:
    async def root(self) -> bool:
        return True

