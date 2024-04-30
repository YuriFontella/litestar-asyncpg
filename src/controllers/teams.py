import random

from litestar import Router, get, post, Request
from litestar.types import Scope
from asyncpg import Connection

from src.middlewares.auth import AuthenticationMiddleware
from src.structs.main import TeamsPlayers


@post(path='/players')
async def post_players(data: TeamsPlayers, db_connection: Connection, scope: Scope, request: Request) -> bool:
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

            request.app.emit('messages', 'Seu time foi criado com sucesso!')

    return True


@get(path='/players', cache=4)
async def get_players(db_connection: Connection) -> list[TeamsPlayers]:
    teams = await db_connection.fetch('select * from teams')

    response = []
    if teams:
        for t in teams:
            team = {
                'id': t['id'],
                'name': t['name'],
                'price': t['price'],
                'owner': t['owner'],
                'date': t['date'],
                'players': []
            }

            players = await db_connection.fetch('select * from players where team_id = $1', t['id'])
            for p in players:
                player = {
                    'id': p['id'],
                    'name': p['name'],
                    'language': p['language'],
                    'status': p['status']
                }

                team['players'].append(player)

            response.append(team)

    return [TeamsPlayers(**i) for i in response]


router = Router(path='/teams', route_handlers=[post_players, get_players], middleware=[AuthenticationMiddleware])
