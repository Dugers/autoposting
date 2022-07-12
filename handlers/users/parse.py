from loader import dp
from filters import OnlyAdminFilter
from aiogram.types import Message
from utils.db import get_groups, create_content, get_content, create_post, get_post, update_post
from utils.vk_api import parse_posts


@dp.message_handler(OnlyAdminFilter(), lambda message: message.text.lower() == "парсинг контента с груп")
async def parse_content(message: Message):
    await message.answer("✅ Начинаю парсинг (Можете продолжать пользоваться ботом, я сообщу о готовности )\n⚠️ Во время поиска рекомендуется не создавать новые посты на основе собранного контента")
    count = 0
    groups = await get_groups()
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
        await message.answer("❌ Увы, новых записей не найдено\nРекомендация:\n⚠️ Осуществляйте парсинг не чаще чем раз в час")
    else:
        await message.answer(f"✅ Готово, добавленно <b>{count}</b> постов")