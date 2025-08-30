UPSERT_TEAM = """
    insert into teams (name, price, protocol, owner)
    values ($1, $2, $3, $4)
    on conflict (name)
    do update set price = excluded.price
    returning id
"""

LIST_TEAMS = """
    select * from teams
"""

LIST_PLAYERS_BY_TEAM = """
    select * from players where team_id = $1
"""
