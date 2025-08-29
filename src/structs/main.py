# Este arquivo agora importa as entidades comuns para manter compatibilidade
# com o código existente que usa estas classes

from src.domain.entities.common import User, Team as Teams, Player as Players, Token


# Classe de compatibilidade para manter a API existente
class TeamsPlayers(Teams):
    """Classe de compatibilidade para TeamsPlayers."""
    players: list[Players]
