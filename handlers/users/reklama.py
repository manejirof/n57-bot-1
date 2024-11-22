from data.settings import *
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from data.database import db
from keyboards.inline.main_inline import *
from data.config import ADMINS


@dp.message(F.text=='rek')
async def rek(message:Message):
    if message.from_user.id == int(ADMINS):
        await message.answer("Admin rek yuboring")
    else:
        await message.answer("Siz admin emassiz")


