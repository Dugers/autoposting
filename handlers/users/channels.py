from loader import dp
from filters import OnlyAdminFilter
from states import ChannelState
from utils.db import get_channels, create_channel, delete_channel
from keyboards.inline import channels_keyboard, full_channels_keyboard, channel_return, cancel_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery


@dp.message_handler(OnlyAdminFilter(), lambda message: message.text.lower() == "список каналов")
async def channels_list(message: Message):
    channels = await get_channels()
    keyboard = channels_keyboard
    if len(channels) == 0:
        text = "Каналы еще не были добавлены"
    else:
        keyboard = full_channels_keyboard
        text = "ID                            | Название канала"
        for channel in channels:
            text += f"\n{channel['id']} | {channel['name']}"
    await message.answer(text, reply_markup=keyboard)


@dp.channel_post_handler(lambda message: message.text.lower() == "добавить постинг")
async def channels_posts(message: Message):
    await message.delete()
    channel_id = message.chat.id
    channel_name = message.chat.title
    result = await get_channels(id=channel_id)
    if result is None:
        await create_channel(id=channel_id, name=channel_name)


@dp.callback_query_handler(text="channel_return")
async def return_to_channel_list(callback: CallbackQuery):
    await callback.message.delete()
    await channels_list(callback.message)


@dp.callback_query_handler(text="cancel", state=ChannelState.channel_id)
async def cancel_del_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await channels_list(callback.message)


@dp.callback_query_handler(text="add_channel")
async def add_channel_guide(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Инструкция по добавлению канала:\nДобавьте бота в свой канал\nСделайте пост "Добавить постинг"\nЕсли бот автоматически удалил ваше сообщение, то канал должен появиться в списке', reply_markup=channel_return)


@dp.callback_query_handler(text="del_channel")
async def del_channel_set(callback: CallbackQuery, state: FSMContext):
    await ChannelState.channel_id.set()
    await callback.message.delete()
    msg = await callback.message.answer("Введите id канала (указывать нужно вместе с минусом)", reply_markup=cancel_keyboard)
    async with state.proxy() as data:
        data['msg'] = msg


@dp.message_handler(state=ChannelState.channel_id)
async def del_channel(message: Message, state: FSMContext):
    async with state.proxy() as data:
        msg = data['msg']
        await msg.delete()
        if not (message.text[1:].isdigit()):
            msg = await message.answer("ID введен не правильно, отправьте мне цифры\nПопробуйте снова", reply_markup=cancel_keyboard)
            data['msg'] = msg
            return
        channel_info = await get_channels(id=int(message.text))
        if channel_info is None:
            msg = await message.answer("ID введен не правильно, канала с таким ID не существует\nПопробуйте снова", reply_markup=cancel_keyboard)
            data['msg'] = msg
            return
        else:
            await state.finish()
            await delete_channel(id=int(message.text))
            await message.answer("Успешно")
            await channels_list(message)