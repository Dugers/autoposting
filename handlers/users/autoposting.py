from handlers.users.groups import cancel
from loader import dp
from states import AutopostingState
from utils.db import get_autoposting, get_channels, update_autoposting
from keyboards.inline import autoposting_disabled_keyboard, autoposting_enabled_keyboard, autoposting_settings_keyboard, cancel_keyboard, autoposting_settings_channels_keyboard
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery


@dp.message_handler(lambda message: message.text.lower() == "автопостинг")
async def autoposting_info(message: Message):
    autoposting_info = await get_autoposting()
    status = ""
    if autoposting_info['status']:
        status = "Включен"
        keyboard = autoposting_enabled_keyboard
    else:
        status = "Выключен"
        keyboard = autoposting_disabled_keyboard
    channels_list = "Список каналов:\n ID                            | Название"
    if autoposting_info['channels_ids'] is None:
        channels_list = "Каналы не были добавлены"
    else:
        for i in autoposting_info['channels_ids']:
            channel = await get_channels(id=i)
            channels_list += f"\n{channel['id']} | {channel['name']}"
    await message.answer(f"Автопостинг\nСостояние: {status}\nТаймаут между постами: {autoposting_info['timeout']} минуты\n{channels_list}", reply_markup=keyboard)


@dp.callback_query_handler(text="autoposting_settings")
async def autoposting_settings(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Настройки:", reply_markup=autoposting_settings_keyboard)


@dp.callback_query_handler(text="autoposting_settings_return")
async def return_to_autoposting_menu(callback: CallbackQuery):
    await callback.message.delete()
    await autoposting_info(callback.message)


@dp.callback_query_handler(text="cancel", state=AutopostingState)
async def cancel_autoposting_settings(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await autoposting_info(callback.message)


@dp.callback_query_handler(text="autoposting_settings_timeout")
async def autoposting_settings_timeout(callback: CallbackQuery, state: FSMContext):
    await AutopostingState.data.set()
    async with state.proxy() as data:
        data['settings'] = "timeout"
    await callback.message.delete()
    await callback.message.answer("Введите целое число в диапазоне от 1 до 1440\nСистема измерения минуты", reply_markup=cancel_keyboard)


@dp.callback_query_handler(text="autoposting_settings_channels")
async def autoposting_settings_channels(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    channels_list = await get_channels()
    if len(channels_list) == 0:
        await callback.message.answer("Нету добавленных каналов, сначала подключите каналы")
        return
    await AutopostingState.data.set()
    async with state.proxy() as data:
        data['settings'] = "channels"
        data['channels'] = []
    text = "Введите ID канала который хотите добавить\nВводите ID по одному\nКогда будет готово нажмите 'Всё'\n ID                            | Название"
    for channel in channels_list:
        text += f"\n{channel['id']} | {channel['name']}"
    await callback.message.answer(text, reply_markup=cancel_keyboard)

@dp.message_handler(state=AutopostingState.data)
async def autoposting_settings_set(message: Message, state: FSMContext):
    if not (message.text.isdigit() or message.text[1:].isdigit()):
        await message.answer("Отправьте число", reply_markup=cancel_keyboard)
        return
    async with state.proxy() as data:
        if data['settings'] == "timeout":
            if int(message.text) > 1440 or int(message.text) < 1:
                await message.answer("Число выходит за пределы\nОтправьте число в диапазоне от 1 до 1440", reply_markup=cancel_keyboard)
            else:
                await update_autoposting(timeout=int(message.text))
                await message.answer("Успешно")
                await state.finish()
                await autoposting_info(message)
        elif data['settings'] == "channels":
            channel_info = await get_channels(id=int(message.text))
            if channel_info is None:
                await message.answer("Канала с таким ID не существует\nПопробуйте снова", reply_markup=cancel_keyboard)
            else:
                data['channels'].append(int(message.text))
                await message.answer("ID добавлен\nВы можете отправить еще ID или нажмать 'Всё', чтобы сохранить изменени", reply_markup=autoposting_settings_channels_keyboard)


@dp.callback_query_handler(text="autoposting_channels_ready", state=AutopostingState.data)
async def autoposting_update_channels_ids(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        channels_ids = data['channels']
        await update_autoposting(channels_ids=channels_ids)
    await state.finish()
    await callback.message.answer("Готово")
    await autoposting_info(callback.message)


@dp.callback_query_handler(text="autoposting_enable")
async def autoposting_enable(callback: CallbackQuery):
    autoposting = await get_autoposting()
    if autoposting['channels_ids'] is None:
        await callback.message.delete()
        await callback.message.answer("Сначала добавьте каналы")
        await autoposting_info(callback.message)
        return
    else:
        await callback.message.delete()
        await update_autoposting(status_enable=True)
        await autoposting_info(callback.message)
        return


@dp.callback_query_handler(text="autoposting_disable")
async def autoposting_disable(callback: CallbackQuery):
    await callback.message.delete()
    await update_autoposting(status_disable=True)
    await autoposting_info(callback.message)