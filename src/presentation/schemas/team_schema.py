from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from msgspec import Struct

# Importando as entidades comuns
from src.domain.entities.common import Team, Player
from src.domain.entities.base import BaseEntity


class PlayerSchema(BaseEntity, kw_only=True):
    """Schema para jogador."""
    id: Optional[int] = None
    language: Optional[str] = 'pt-br'
    uuid: Optional[str] = None
    status: Optional[bool] = False
    team_id: Optional[int] = None
    name: str
    
    def to_entity(self) -> Player:
        """Converte o schema para entidade Player."""
        return Player(**self.to_dict())
    
    @classmethod
    def from_entity(cls, entity: Player) -> 'PlayerSchema':
        """Cria um schema a partir de uma entidade Player."""
        return cls(**entity.to_dict())


class TeamSchema(BaseEntity, kw_only=True):
    """Schema para equipe."""
    id: Optional[int] = None
    owner: Optional[str] = None
    protocol: Optional[int] = None
    date: Optional[datetime] = None
    players: Optional[List[PlayerSchema]] = None
    name: str
    price: Decimal
    
    def to_entity(self) -> Team:
        """Converte o schema para entidade Team."""
        team_data = self.to_dict()
        players_data = team_data.pop('players', None)
        team = Team(**team_data)
        
        if players_data:
            team.players = [player.to_entity() for player in players_data]
            
        return team
    
    @classmethod
    def from_entity(cls, entity: Team) -> 'TeamSchema':
        """Cria um schema a partir de uma entidade Team."""
        team_data = entity.to_dict()
        players_data = team_data.pop('players', None)
        
        team_schema = cls(**team_data)
        
        if players_data:
            team_schema.players = [PlayerSchema.from_entity(player) for player in players_data]
            
        return team_schema