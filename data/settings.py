from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from data.config import BOT_TOKEN


bot = Bot(token = BOT_TOKEN, default = DefaultBotProperties(
    parse_mode = ParseMode.HTML,
))

dp=Dispatcher()
