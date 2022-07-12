from .conn import get_conn


async def delete_group(id=False, name=False):
    conn = await get_conn()
    if id:
        await conn.execute('DELETE FROM groups WHERE id = $1', id)
    elif name:
        await conn.execute('DELETE FROM groups WHERE url_name = $1', name)
    await conn.close()


async def delete_other_contents(id):
    conn = await get_conn()
    await conn.execute('DELETE FROM other_contents WHERE id = $1', id)
    await conn.close()


async def delete_contents(id):
    conn = await get_conn()
    await conn.execute('DELETE FROM contents WHERE id = $1', id)
    await conn.close()


async def delete_channel(id):
    conn = await get_conn()
    await conn.execute('DELETE FROM channels WHERE id = $1', id)
    await conn.close()