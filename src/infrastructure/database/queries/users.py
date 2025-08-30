FIND_BY_EMAIL = """
    select id, name, email, password, role, status
    from users
    where email = $1
    limit 1
"""

CREATE_USER = """
    insert into users (name, email, password, role, status)
    values ($1, $2, $3, $4, coalesce($5, true))
    returning id
"""

FIND_ACTIVE_BY_EMAIL = """
    select id, name, email, password, role, status
    from users
    where email = $1 and status = true
    limit 1
"""
