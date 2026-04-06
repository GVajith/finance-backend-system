from sqlalchemy import select

def get_user_role(conn, user_table, user_id):
    query = select(user_table.c.role).where(user_table.c.id == user_id)
    result = conn.execute(query).fetchone()

    if not result:
        return None

    return result.role