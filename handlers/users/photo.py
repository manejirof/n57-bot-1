import asyncio

from data.settings import bot, dp
from data.config import BOT_TOKEN
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram import types
from rembg import remove
from PIL import Image
import time
import requests
from data.database import db
from keyboards.inline.main_inline import home


@dp.message(F.photo)
async def remgb_image(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id=file_id)
    time_await = await message.reply("""

                    ⌛️ <i>rasmga ishlov berilmoqda</i> ✏️
                    □□□□□□□□□□ 0%
                                      """)
    file_path = file.file_path
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    time_ = time.time()
    name = f"{message.from_user.id}_{time_}.png"
    input_path = requests.get(url=url, stream=True).raw
    output_path = name
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)
    rasm = types.input_file.FSInputFile(name)
    user_data = db.user_info(telegram_id=message.from_user.id)
    balance = user_data.get('balance')
    if balance is not None:
        balance = int(balance)
        if balance >= 500:
            db.update_user_balance(
                balance=balance - 500,
                telegram_id=message.from_user.id
            )


    await message.reply_photo(photo=rasm,
                              caption=f"🤖<b>: Rasm orqa foni olib tashlandi</b>\n🤖<b>:</b><i>Menga yana rasm yuborishingiz mumkin ☺️</i>")
    await time_await.delete()
    data_balance = await message.answer(text="balanc -500 som")
    await asyncio.sleep(5)
    await data_balance.delete()


@dp.callback_query(F.data=='rembg')
async def rembg_func(call: CallbackQuery):
    await call.answer('page selection')

# @dp.message(F.photo)
# async def remgb_image(message: Message):
#     photo = message.photo[-1]
#     file_id = photo.file_id
#     file = await bot.get_file(file_id=file_id)
#     time_await = await message.reply("""
#
#                     ⌛️ <i>rasmga ishlov berilmoqda</i> ✏️
#                     □□□□□□□□□□ 0%
#                                       """)
#     file_path = file.file_path
#     url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
#     time_ = time.time()
#     name = f"{message.from_user.id}_{time_}.png"
#     input_path = requests.get(url=url, stream=True).raw
#     output_path = name
#     input = Image.open(input_path)
#     output = remove(input)
#     output.save(output_path)
#     rasm = types.input_file.FSInputFile(name)
#     await message.reply_photo(photo=rasm,
#                               caption=f"🤖<b>: Rasm orqa foni olib tashlandi</b>\n🤖<b>:</b><i>Ishim sifatini baxolashni unutmang ☺️</i>")
#     await time_await.delete()
#     await message.answer("Menu", reply_markup=home)