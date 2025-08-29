from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Importando as entidades comuns
from src.domain.entities.common import Team as TeamEntity, Player as PlayerEntity


# Classes de compatibilidade usando dataclass para manter a API existente
@dataclass
class Player(PlayerEntity):
    """Classe de compatibilidade para Player usando dataclass."""
    pass


@dataclass
class Team(TeamEntity):
    """Classe de compatibilidade para Team usando dataclass."""
    date: Optional[datetime] = field(default_factory=datetime.now)
    players: Optional[List[Player]] = field(default_factory=list)