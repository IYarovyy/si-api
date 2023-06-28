from quart import current_app
from quart import Quart


async def insert_user(data: dict):
    insert = """
    INSERT INTO users(urole, email, password) VALUES($1, $2, $3)
    """
    urole = data.get("urole")
    email = data.get("email")
    password = data.get("password")

    async with current_app.db_pool.acquire() as conn:
        return await conn.execute(insert, urole, email, password)


# For use in command line only. Don't use it in controllers
async def add_user(data: dict, app: Quart):
    insert = """
    INSERT INTO users(urole, email, password) VALUES($1, $2, $3)
    """
    urole = data.get("urole")
    email = data.get("email")
    password = data.get("password")

    async with app.db_pool.acquire() as conn:
        return await conn.execute(insert, urole, email, password)


async def find_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE id = $1"

    async with current_app.db_pool.acquire() as conn:
        return conn.fetchrow(query, user_id)


async def find_user_by_email(email: str):
    query = "SELECT * FROM users WHERE email = $1"

    async with current_app.db_pool.acquire() as conn:
        return await conn.fetchrow(query, email)
