from typing import List, Any

from src.domain.entities.common import Team, Player
from src.domain.interfaces.repositories import TeamRepositoryInterface, PlayerRepositoryInterface
from src.infrastructure.database.connection import DatabaseConnection


class TeamRepository(TeamRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def create(self, team: Team) -> int:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = '''
                insert into teams (name, price, protocol, owner)
                values ($1, $2, $3, $4)
                on conflict (name) 
                do update set price = excluded.price
                returning id
            '''
            
            result = await conn.fetchval(
                query,
                team.name,
                team.price,
                team.protocol,
                team.owner
            )
            
            return result

    async def get_all(self) -> List[Team]:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = "select * from teams"
            records = await conn.fetch(query)
            
            teams = []
            for record in records:
                teams.append(Team(
                    id=record['id'],
                    name=record['name'],
                    price=record['price'],
                    owner=record['owner'],
                    protocol=record['protocol'],
                    date=record['date'],
                    players=[]
                ))
            
            return teams


class PlayerRepository(PlayerRepositoryInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def create_many(self, players: List[Player]) -> bool:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            data = [(player.name, player.team_id) for player in players]
            await conn.executemany(
                'insert into players (name, team_id) values ($1, $2)',
                data
            )
            return True

    async def get_by_team_id(self, team_id: int) -> List[Player]:
        app_state = Any  # Será substituído pelo estado real da aplicação
        async with await self.db_connection.get_connection(app_state) as conn:
            query = "select * from players where team_id = $1"
            records = await conn.fetch(query, team_id)
            
            players = []
            for record in records:
                players.append(Player(
                    id=record['id'],
                    name=record['name'],
                    language=record['language'],
                    uuid=record['uuid'],
                    status=record['status'],
                    team_id=record['team_id']
                ))
            
            return players