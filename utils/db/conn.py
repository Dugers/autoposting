import asyncpg
from data import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE


async def get_conn():
    return await asyncpg.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)