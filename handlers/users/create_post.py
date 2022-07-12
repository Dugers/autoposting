from loader import dp, bot
from filters import OnlyAdminFilter
from states import PostState
from utils.db import get_post, get_content, create_other_content, get_other_content, update_post, delete_other_contents, delete_contents, get_channels
from keyboards.inline import post_edit_menu_keyboard, send_photo_video_keyboard, cancel_keyboard, cancel_or_none_text_keyboard
from aiogram.types import Message, CallbackQuery, MediaGroup, InputMediaVideo
from aiogram.dispatcher import FSMContext



@dp.message_handler(OnlyAdminFilter(), lambda message: message.text.lower() == "добавить новый пост")
async def create_post(message: Message, state: FSMContext):
    post = await get_post(not_checked=True)
    if post is None:
        await message.answer("В данный момент контента для постов нету, попробуйте спарсить контент с груп")
        return
    await PostState.method.set()
    contents = await get_content(post_id=post['id'])
    other_contents = await get_other_content(post_id=post['id'])
    description = post['description']
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
    msg = await message.answer_media_group(media=media)
    text = "Редактирование:"
    if not (description is None):
        text = description
    msg2 = await message.answer(text, reply_markup=post_edit_menu_keyboard)
    async with state.proxy() as data:
        data['msg'] = msg
        data['msg2'] = msg2
        data['post_id'] = post['id']
        if post['contents_ids'] is None:
            data['post_contents'] = []
        else:
            data['post_contents'] = post['contents_ids']
        if post['other_content_ids'] is None:
            data['post_other_contents'] = []
        else:
            data['post_other_contents'] = post['other_content_ids']
        data['description'] = description


@dp.callback_query_handler(text="cancel", state=PostState)
async def cancel_edit_post(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
    await msg.delete()
    await state.finish()
    await create_post(callback.message, state)


@dp.callback_query_handler(text="cancel_publish_post", state=PostState.method)
async def cancel_publish_post(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        msg = data['msg']
        msg2 = data['msg2']
    await msg2.delete()
    for i in msg:
        await i.delete()
    await state.finish()


@dp.callback_query_handler(text="edit_add_text", state=PostState.method)
async def edit_text_post(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        msg2 = data['msg2']
        for i in msg:
            await i.delete()
        await msg2.delete()
        if data['description'] is None:
            keyboard = cancel_keyboard
        else:
            keyboard = cancel_or_none_text_keyboard
        msg = await callback.message.answer("Введите текст", reply_markup=keyboard)
        data['msg'] = msg
        data['method'] = "add_text"
    await PostState.next()


@dp.callback_query_handler(text="none_text", state=PostState.data)
async def add_none_text(callback: CallbackQuery, state: FSMContext):
    callback.message.text = None
    await add_text(callback.message, state)


@dp.message_handler(state=PostState.data)
async def add_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if data['method'] != "add_text":
            if data['method'] == "posting":
                await publish_post(message, state)
            return
        msg = data['msg']
        await msg.delete()
        await update_post(data['post_id'], description=message.text)
    await state.finish()
    await message.answer("Текст успешно изменен")
    await create_post(message, state)


@dp.callback_query_handler(lambda callback: callback.data.endswith('_add_media'), state=PostState.method)
async def add_media_post(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        msg2 = data['msg2']
        for i in msg:
            await i.delete()
        await msg2.delete()
        msg = await callback.message.answer("Отправьте фото или видео (Отправляйте по одному)", reply_markup=cancel_keyboard)
        data['msg'] = msg
        data['method'] = callback.data.replace("edit_","")
        if data['method'] == "add_media":
            data['lenght'] = 10 - len(data['post_contents']) - len(data['post_other_contents'])
        else:
            data['lenght'] = 10
        data['results'] = []
    await PostState.next()


@dp.message_handler(content_types=['photo'], state=PostState.data)
async def add_media(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        await msg.delete()
        if len(data['results']) > data['lenght'] - 1:
            msg = await message.answer("Этот файл не был добавлен, вы уже добавили максимальное количество фото/видео\nНажмите 'Всё' для сохранение", reply_markup=send_photo_video_keyboard)
        elif len(data['results']) == data['lenght'] - 1:
            data['results'].append(['photo', message.photo[0].file_id])
            msg = await message.answer("Добавлено максимальное количество фото/видео\nНажмите 'Всё' для сохранения", reply_markup=send_photo_video_keyboard)
        else:
            data['results'].append(['photo', message.photo[0].file_id])
            msg = await message.answer(f"Отправлено {len(data['results'])} файлов\nМаксимальное количество {data['lenght']}\nКогда будет готово нажмите кнопку 'Всё'", reply_markup=send_photo_video_keyboard)
        data['msg'] = msg
 

@dp.message_handler(content_types=['video'], state=PostState.data)
async def add_media(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        await msg.delete()
        if len(data['results']) > data['lenght'] - 1:
            msg = await message.answer("Этот файл не был добавлен, вы уже добавили максимальное количество фото/видео\nНажмите 'Всё' для сохранение", reply_markup=send_photo_video_keyboard)
        elif len(data['results']) == data['lenght'] - 1:
            data['results'].append(['video', message.video.file_id])
            msg = await message.answer("Добавлено максимальное количество фото/видео\nНажмите 'Всё' для сохранения", reply_markup=send_photo_video_keyboard)
        else:
            data['results'].append(['video', message.video.file_id])
            msg = await message.answer(f"Отправлено {len(data['results'])} файлов\nМаксимальное количество {data['lenght']}\nКогда будет готово нажмите кнопку 'Всё'", reply_markup=send_photo_video_keyboard)
        data['msg'] = msg


@dp.callback_query_handler(text="ready_add_photo_video", state=PostState.data)
async def edit_post_media(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        await msg.delete()
        post_id = data['post_id']
        post_contents_ids = data['post_contents']
        post_other_contents = data['post_other_contents']
        other_contents = data['results']
        method = data['method']
    await state.finish()
    if method == "del_and_add_media":
        for other_content in post_other_contents:
            await delete_other_contents(other_content)
        for content in post_contents_ids:
            await delete_contents(content)
        post_contents_ids = []
        post_other_contents = []
    for other_content in other_contents:
        await create_other_content(post_id=post_id, content_type=other_content[0], file_id=other_content[1])
    else:
        result = await get_other_content(post_id=post_id)
        for other_content in result:
            post_other_contents.append(other_content['id'])
    await update_post(id=post_id, contents_ids=post_contents_ids, other_content_ids=post_other_contents)
    # await callback.message.answer("Успешно\nРезультат:")
    await create_post(callback.message, state)


@dp.callback_query_handler(text="publish_post", state=PostState.method)
async def select_channel_publish_post(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        msg2 = data['msg2']
        for i in msg:
            await i.delete()
        await msg2.delete()
        channels = await get_channels()
        if len(channels) == 0:
            data['msg'] = await callback.message.answer("Добавьте каналы для постинга", reply_markup=cancel_keyboard)
            return
        text = "Введите ID канала в который хотите запостить контент\nID                            | Название"
        for channel in channels:
            text += f"\n{channel['id']} | {channel['name']}"
        msg = await callback.message.answer(text, reply_markup=cancel_keyboard)
        data['msg'] = msg
        data['method'] = "posting"
        await PostState.next()


async def publish_post(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        await msg.delete()
        if not (message.text[1:].isdigit()):
            data['msg'] = await message.answer("ID канала введен не правильно, отправьте цифру\nПопробуйте снова", reply_markup=cancel_keyboard)
            return
        channel_info = await get_channels(id=int(message.text))
        if channel_info is None:
            data['msg'] = await message.answer("ID канала указан не правильно, такого канала не существует\nПопробуйте снова", reply_markup=cancel_keyboard)
            return
        else:
            await message.answer("Пост публикуется...")
            res = await publish_post_in_channel(int(message.text), data['post_id'])
            if not (res is None) and res == False:
                await message.answer("Пост не был опубликован\nПроблемы с правами бота, проверьте наличие бота в вашем канале, а также его права на публикацию постов")
            if res:
                await message.answer("Пост успешно опубликован")
    await state.finish()
    await create_post(message, state)


async def publish_post_in_channel(channel_id, post_id):
    post_info = await get_post(id=post_id)
    description = post_info['description']
    contents = await get_content(post_id=post_id)
    other_contents = await get_other_content(post_id=post_id) 
    media = MediaGroup()
    for content in contents:
        caption = None
        if content == contents[0]:
            caption = description
        if content['content_type'] == "photo":
            media.attach_photo(content['url'], caption=caption)
        elif content['content_type'] == "video":
            media.attach_video(InputMediaVideo(content['url']), caption=caption)
    for content in other_contents:
        caption = None
        if (content == other_contents[0]) and len(contents) == 0:
            caption = description
        if content['content_type'] == "photo":
            media.attach_photo(content['file_id'], caption=caption)
        elif content['content_type'] == "video":
            media.attach_video(InputMediaVideo(content['file_id']), caption=caption)
    try:
        await bot.send_media_group(channel_id, media)
        await update_post(post_id, cheched_published=True)
        return True
    except:
        return False


@dp.callback_query_handler(text="del_post", state=PostState.method)
async def del_post(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        msg2 = data['msg2']
        for i in msg:
            await i.delete()
        await msg2.delete()
        await update_post(data['post_id'], checked_not_published=True)
    await state.finish()
    await create_post(callback.message, state)