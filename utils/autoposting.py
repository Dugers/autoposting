import asyncio
from loader import bot
from data import ADMINS_IDS
from utils.db import get_autoposting, get_post, update_post, get_content, get_other_content, get_groups, create_content, create_post
from utils.vk_api import parse_posts
from aiogram.types import MediaGroup, InputMediaVideo


async def autoposting(autoposting_info):
    post_info = await get_post(not_checked=True)
    if post_info is None:
        for admin in ADMINS_IDS:
            await bot.send_message(admin, "Посты закончились, начинаю парсинг новых постов")
        need_continue = await parse_content()
        if need_continue:
            post_info = await get_post(not_checked=True)
            for admin in ADMINS_IDS:
                await bot.send_message(admin, "Ура\nНовые посты были найдены")
        else:
            for admin in ADMINS_IDS:
                await bot.send_message(admin, "Нету новых постов для автопостинга\nСоветы:\nДобавьте больше груп\nУвеличьте таймаут\nВыключите бота до момента появления новых постов")
            return
    contents = await get_content(post_id=post_info['id'])
    other_contents = await get_other_content(post_id=post_info['id']) 
    media = MediaGroup()
    for content in contents:
        if content['content_type'] == "photo":
            media.attach_photo(content['url'])
        elif content['content_type'] == "video":
            media.attach_video(InputMediaVideo(content['url']))
    for content in other_contents:
        if content['content_type'] == "photo":
            media.attach_photo(content['file_id'])
        elif content['content_type'] == "video":
            media.attach_video(InputMediaVideo(content['file_id']))
    await update_post(post_info['id'], cheched_published=True)
    for channel in autoposting_info['channels_ids']:
        try:
            await bot.send_media_group(channel, media)
        except:
            for admin in ADMINS_IDS:
                await bot.send_message(admin, f"Не удалось отправить сообщение в канал с ID {channel}\nВозможные причины:\nБот был удален из группы\nУ бота нету прав для отправки постов")



async def parse_content():
    groups = await get_groups()
    count = 0
    for group in groups:
        posts = await parse_posts(group['url_name'])
        for i in range(len(posts) - 1, -1, -1):
            post = posts[i]
            content = await get_content(post[1])
            if not (content is None):
                break
            await create_content(post[1], post[2], post[0], post[3])
            post_info = await get_post(post[0])
            if post_info is None:
                count += 1
                await create_post(post[0], post[1])
            else:
                contents_ids = post_info['contents_ids']
                contents_ids.append(post[1])
                await update_post(post[0], contents_ids=contents_ids)
    if count == 0:
        return False
    else:
        return True



async def schedule():
    while True:
        autoposting_info = await get_autoposting()
        if autoposting_info['status']:
            await autoposting(autoposting_info)
        await asyncio.sleep(autoposting_info['timeout']*60)