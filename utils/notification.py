import asyncio

from data.settings import bot, dp
from data.config import ADMINS
from data.database import db

async def start():
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text='bot faol holatda')


async def shutdown():
    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text='bot faol holatda emas')



