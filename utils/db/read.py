from .conn import get_conn


async def get_groups(id=False, name=False):
    conn = await get_conn()
    if id:
        res = await conn.fetchrow('SELECT * FROM groups WHERE id = $1', id)
    elif name:
        res = await conn.fetchrow('SELECT * FROM groups WHERE url_name = $1', name)
    else:
        res = await conn.fetch('SELECT * FROM groups')
    await conn.close()
    return res


async def get_content(id=False, post_id=False):
    conn = await get_conn()
    if id:
        res = await conn.fetchrow('SELECT * FROM contents WHERE id = $1', id)
    if post_id:
        res = await conn.fetch('SELECT * FROM contents WHERE post_id = $1', post_id)
    await conn.close()
    return res


async def get_post(id=False, not_checked=False):
    conn = await get_conn()
    if id:
        res = await conn.fetchrow('SELECT * FROM posts WHERE id = $1', id)
    if not_checked:
        res = await conn.fetchrow('SELECT * FROM posts WHERE checked = false ORDER BY id')
    await conn.close()
    return res


async def get_other_content(post_id):
    conn = await get_conn()
    if post_id:
        res = await conn.fetch('SELECT * FROM other_contents WHERE post_id = $1', post_id)
    await conn.close()
    return res


async def get_channels(id=False):
    conn = await get_conn()
    if id:
        res = await conn.fetchrow('SELECT * FROM channels WHERE id = $1', id)
    else:
        res = await conn.fetch('SELECT * FROM channels')
    await conn.close()
    return res


async def get_autoposting(conn=False):
    if conn:
        return await conn.fetchrow('SELECT * FROM autoposting')
    else:
        conn = await get_conn()
        res = await conn.fetchrow('SELECT * FROM autoposting')
        await conn.close()
        return res