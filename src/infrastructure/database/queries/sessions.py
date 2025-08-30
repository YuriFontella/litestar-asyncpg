CREATE_SESSION = """
    insert into sessions (access_token, user_agent, ip, user_id)
    values ($1, $2, $3, $4) returning id
"""
