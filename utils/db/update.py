from .conn import get_conn


async def update_post(id, contents_ids=False, description=False, other_content_ids=False, cheched_published=False, checked_not_published=False):
    conn = await get_conn()
    if contents_ids:
        await conn.execute('UPDATE posts SET contents_ids = $1 WHERE id = $2', contents_ids, id)
    if (description is None) or description:
        await conn.execute('UPDATE posts SET description = $1 WHERE id = $2', description, id)
    if other_content_ids:
        await conn.execute('UPDATE posts SET other_content_ids = $1 WHERE id = $2', other_content_ids, id)
    if cheched_published:
        await conn.execute('UPDATE posts SET checked = true, published = true WHERE id = $1', id)
    if checked_not_published:
        await conn.execute('UPDATE posts SET checked = true WHERE id = $1', id)
    await conn.close()


async def update_autoposting(status_enable=False, status_disable=False, channels_ids=False, timeout=False):
    conn = await get_conn()
    if status_enable:
        await conn.execute('UPDATE autoposting SET status = true')
    if status_disable:
        await conn.execute('UPDATE autoposting SET status = false')
    if channels_ids:
        await conn.execute('UPDATE autoposting SET channels_ids = $1', channels_ids)
    if timeout:
        await conn.execute('UPDATE autoposting SET timeout = $1', timeout)
    await conn.close()