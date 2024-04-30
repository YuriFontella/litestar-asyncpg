import random

from litestar import Router, get, post
from litestar.types import Scope
from asyncpg import Connection

from src.middlewares.auth import AuthenticationMiddleware
from src.structs.main import TeamsPlayers


@post(path='/players')
async def post_players(data: TeamsPlayers, db_connection: Connection, scope: Scope) -> bool:
    async with db_connection.transaction():
        user = scope.get('user')
        user = await db_connection.fetchrow('select name from users where id = $1', user)

        protocol = random.randint(111111, 999999)

        query = '''
            insert into teams (name, price, protocol, owner)
            values ($1, $2, $3, $4)
            on conflict (name) 
            do update set price = excluded.price
            returning id
        '''
        team = await db_connection.fetchrow(query, data.name, data.price, protocol, user['name'])
        if team:
            data = [(i.name, team['id']) for i in data.players]
            await db_connection.executemany('insert into players (name, team_id) values ($1, $2)', data)

    return True


@get(path='/players', cache=4)
async def get_players(db_connection: Connection) -> list[TeamsPlayers]:
    teams = await db_connection.fetch('select * from teams')
    if teams:
        response = []
        for i in teams:
            players = await db_connection.fetch('select * from players where team_id = $1', i['id'])
            response.append({**i, 'players': [dict(i) for i in players]})

        return [TeamsPlayers(**i) for i in response]


router = Router(path='/teams', route_handlers=[post_players, get_players], middleware=[AuthenticationMiddleware])
