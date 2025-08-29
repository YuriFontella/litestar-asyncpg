from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

# Importando as entidades comuns
from src.domain.entities.common import User as UserEntity, Session as SessionEntity


# Classes de compatibilidade usando dataclass para manter a API existente
@dataclass
class User(UserEntity):
    """Classe de compatibilidade para User usando dataclass."""
    pass


@dataclass
class Session(SessionEntity):
    """Classe de compatibilidade para Session usando dataclass."""
    date: Optional[datetime] = field(default_factory=datetime.now)