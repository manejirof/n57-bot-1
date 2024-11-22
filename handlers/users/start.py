import asyncio

from data.settings import *
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from data.database import db
from keyboards.default.main_button import buton
from keyboards.inline.main_inline import *


@dp.message(CommandStart())
async def start(msg: Message):
    telegram_id = msg.from_user.id
    telegram_full_name = msg.from_user.full_name
    user = db.sql_check_user(telegram_id=telegram_id)

    if user:
        if not user['first_name'] or not user['last_name'] or not user['gender']:
            await msg.answer(
                "<b>Xizmatlarga kirish cheklangan 🔐\n</b>",
                reply_markup=register_inline
            )
        else:
            await msg.answer(f"<b>Assalomu alaykum, {telegram_full_name} 👋!\n"
                             f"🤖 Botimizga qaytganingizdan xursandmiz! 😊</b>\n"
                             f"<i>Marhamat, xizmatlardan foydalaning!</i>", reply_markup=home)
    else:
        db.register_user(telegram_id, telegram_full_name)
        await msg.answer(f"<b>Assalomu alaykum, {telegram_full_name} 👋!\n"
                         f"Sizni botimizda🤖 ko‘rib turganimizdan juda xursandmiz 😊.</b> "
                         , reply_markup=home_no)



