from .conn import get_conn
from .read import get_autoposting


async def create_tables():
    conn = await get_conn()
    await create_table_groups(conn)
    await create_table_contents(conn)
    await create_table_posts(conn)
    await create_table_other_contents(conn)
    await create_table_channels(conn)
    await create_table_autoposting(conn)
    await conn.close()


async def create_table_groups(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id bigint,
        name text,
        url_name text
    )
    ''')


async def create_table_contents(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS contents (
        id bigint,
        content_type text,
        post_id bigint,
        url text
    )
    ''')


async def create_table_posts(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id bigint,
        contents_ids bigint[],
        other_content_ids integer[],
        description text DEFAULT null,
        checked boolean DEFAULT false,
        published boolean DEFAULT false
    )
    ''')


async def create_table_other_contents(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS other_contents (
        id serial PRIMARY KEY,
        post_id bigint,
        content_type text,
        file_id text
    )
    ''')


async def create_table_channels(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        id bigint,
        name text
    )
    ''')


async def create_table_autoposting(conn):
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS autoposting(
        status boolean DEFAULT false,
        channels_ids bigint[],
        timeout integer DEFAULT 10
    )
    ''')
    autoposting_info = await get_autoposting(conn)
    if autoposting_info is None:
        await create_autoposting(conn)


async def create_group(id, name, url_name):
    conn = await get_conn()
    await conn.execute('INSERT INTO groups(id, name, url_name) VALUES($1, $2, $3)', id, name, url_name)
    await conn.close()


async def create_content(id, content_type, post_id, url):
    conn = await get_conn()
    await conn.execute('INSERT INTO contents(id, content_type, post_id, url) VALUES($1, $2, $3, $4)', id, content_type, post_id, url)
    await conn.close()


async def create_post(id, content_id):
    conn = await get_conn()
    await conn.execute('INSERT INTO posts(id, contents_ids) VALUES($1, $2)', id, [content_id]) 
    await conn.close()


async def create_other_content(post_id, content_type, file_id):
    conn = await get_conn()
    await conn.execute('INSERT INTO other_contents(post_id, content_type, file_id) VALUES($1, $2, $3)', post_id, content_type, file_id)
    await conn.close()


async def create_channel(id, name):
    conn = await get_conn()
    await conn.execute('INSERT INTO channels(id, name) VALUES($1, $2)', id, name)
    await conn.close()


async def create_autoposting(conn):
    await conn.execute('INSERT INTO autoposting(status) VALUES(false)')