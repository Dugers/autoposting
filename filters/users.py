from data import ADMINS_IDS
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter


class OnlyAdminFilter(BoundFilter):
    def __init__(self, reverse=False):
        self.reverse = reverse
    async def check(self, message: Message):
        if message.from_user.id in ADMINS_IDS:
            if self.reverse:
                return False
            return True
        if self.reverse:
            return True
        return False