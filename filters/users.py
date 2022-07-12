from data import ADMINS_IDS
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class OnlyAdminFilter(BoundFilter):
    async def check(self, message: Message):
        if message.from_user.id in ADMINS_IDS:
            return True
        return False