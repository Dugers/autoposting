import asyncio
from handlers import dp
from aiogram import executor
from filters import setup_filters
from data import ADMINS_IDS, WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT
from loader import bot
from utils.db import create_tables
from utils.autoposting import schedule


async def on_startup(dp):
    await create_tables()
    setup_filters(dp)
    for admin in ADMINS_IDS:
        await bot.send_message(admin, "Bot started working")
    asyncio.create_task(schedule())
    # await bot.set_webhook(WEBHOOK_URL)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )