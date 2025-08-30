from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass(slots=True)
class PlayerIn:
    name: str


@dataclass(slots=True)
class TeamCreateIn:
    name: str
    price: Decimal
    players: List[PlayerIn]

