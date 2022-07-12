from loader import dp
from filters import OnlyAdminFilter
from states import GroupState
from utils.db import get_groups, create_group, delete_group
from utils.vk_api import parse_group_info
from keyboards.inline import groups_menu_keyboard, full_groups_menu_keyboard, cancel_keyboard
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext


@dp.message_handler(OnlyAdminFilter(), lambda message: message.text.lower() == "список груп")
async def groups_list(message: Message):
    groups = await get_groups()
    text = "ID   |    Название    |    Короткое имя(url)"
    for group in groups:
        text += f"\n{group['id']} | {group['name']} | {group['url_name']}"
    keyboard = groups_menu_keyboard
    if len(groups) == 0:
        text = "Увы, группы еще не добавлены, но вы можете их добавить"
    else:
        keyboard = full_groups_menu_keyboard
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(text="cancel", state=GroupState)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    await groups_list(callback.message)


@dp.callback_query_handler(text="add_group")
async def add_group(callback: CallbackQuery, state: FSMContext):
    await GroupState.name_or_id.set()
    async with state.proxy() as data:
        data['method'] = "add"
        data['message'] = callback.message
    await callback.message.edit_text("Введите id группы или ее короткое имя\nПример:\nСсылка на сообщество: https://vk.com/kanal_tv3\nОтправить нужно только <b>kanal_tv3</b>", reply_markup=cancel_keyboard)


@dp.callback_query_handler(text="del_group")
async def del_group(callback: CallbackQuery, state: FSMContext):
    await GroupState.name_or_id.set()
    async with state.proxy() as data:
        data['method'] = "del"
        data['message'] = callback.message
    await callback.message.edit_text("Введите id группы или ее короткое имя\nПример:\nСсылка на сообщество: https://vk.com/kanal_tv3\nОтправить нужно только <b>kanal_tv3</b>", reply_markup=cancel_keyboard)


@dp.message_handler(state=GroupState.name_or_id)
async def method_group(message: Message, state: FSMContext):
    group_id = ""
    group_name = ""
    if message.text.isdigit():
        group_id = int(message.text)
    else:
        message.text = message.text.replace("https://", "")
        message.text = message.text.replace("vk.com/", "")
        message.text = message.text.replace("/", "")
        message.text = message.text.replace(" ", "")
        group_name = message.text
    async with state.proxy() as data:
        method = data['method']
        bot_message = data['message']
    if method == "add":
        if group_id:
            group_info = await parse_group_info(group_id)
        else:
            group_info = await parse_group_info(group_name)
        if group_info:
            if (await get_groups(id=group_info[0])) is None:
                await create_group(group_info[0], group_info[1], group_info[2])
                await bot_message.delete()
                await message.answer("Успешно")
                await state.finish()
                await groups_list(message)
                return
            else:
                await bot_message.delete()
                msg = await message.answer("Такая группа уже добавлена", reply_markup=cancel_keyboard)
        else:
            await bot_message.delete()
            msg = await message.answer("Название группы введено неверно\nПопробуйте снова", reply_markup=cancel_keyboard)
    elif method == "del":
        if group_id:
            group_info = await get_groups(id=group_id)
        else:
            group_info = await get_groups(name=group_name)
        if not (group_info is None):
            if group_id:
                await delete_group(id=group_id)
            else:
                await delete_group(name=group_name)
            await bot_message.delete()
            await message.answer("Успешно")
            await state.finish()
            await groups_list(message)
            return
        else:
            await bot_message.delete()
            msg = await message.answer("Такой группы не существует в списке\nПопробуйте снова", reply_markup=cancel_keyboard)
    async with state.proxy() as data:
        data['message'] = msg