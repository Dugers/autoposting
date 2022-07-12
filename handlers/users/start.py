from loader import dp
from filters import OnlyAdminFilter
from keyboards.default import main_menu_keyboard
from aiogram.types import Message


@dp.message_handler(OnlyAdminFilter(reverse=True))
async def not_admin_message(message: Message):
    await message.answer("У вас недостаточно прав для выполнения этой команды")


@dp.message_handler(OnlyAdminFilter(), commands=['start'])
async def start(message: Message):
    await message.answer("Добавляй группы\nСобирай из них данные\nДобавляй собранные данные в свой канал", reply_markup=main_menu_keyboard)