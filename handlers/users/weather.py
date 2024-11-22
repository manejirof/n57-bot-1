from data.settings import *
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from data.database import db
from keyboards.inline.main_inline import *
from api.weather import get_weather_data

API_TOKEN = "a9520c4fbc4ae75a66b86e6bc5b87896"


@dp.callback_query(City_N.filter())
async def get_weather(call: types.CallbackQuery, callback_data: City_N):
    telegram_id = call.from_user.id
    city_name = callback_data.city
    data = get_weather_data(city_name=city_name)
    city = db.get_city_user(telegram_id, city_name)
    if city:
        await call.answer(f"✅ {city_name.capitalize()} shahar sizning ro'yxatingizda mavjud.", show_alert=True)
        if data:
            await call.message.edit_text(text=data)
            await call.message.edit_reply_markup(reply_markup=delete_city_name(city_name=city_name, telegram_id=telegram_id))
        else:
            await call.message.answer(text=f"<b>Xatolik ketdi🛠</b>\n"
                                           f"<a href='https://t.me/codi_bro'>Admin</a> ga xabar bering",
                                      parse_mode="HTML", disable_web_page_preview=False)

    else:
        await call.answer(f"❌ {city_name.capitalize()} shahar sizning ro'yxatingizda mavjud emas. Shaharni saqlashingiz mumkin", show_alert=True)
        if data:
            await call.message.edit_text(text=data)
            await call.message.edit_reply_markup(reply_markup=save_ciy_name(city_name=city_name, telegram_id=telegram_id))
        else:
            await call.message.answer(text=f"<b>Xatolik ketdi🛠</b>\n"
                                           f"<a href='https://t.me/codi_bro'>Admin</a> ga xabar bering",
                                      parse_mode="HTML", disable_web_page_preview=False)



@dp.callback_query(F.data(startswith="delete_city"))
async def handle_delete_city(call: types.CallbackQuery):

    _, city_name, telegram_id = call.data.split(":")
    telegram_id = int(telegram_id)

    result = db.select_city_delete(telegram_id, city_name)
    if result:
        await call.answer(f"✅ {city_name} shahri muvaffaqiyatli o'chirildi.", show_alert=True)
    else:
        await call.answer(f"❌ {city_name} shahrini o'chirishda xatolik yuz berdi.", show_alert=True)

    await call.message.edit_text(text="Shaharlarni tanlang 👇")
    await call.message.edit_reply_markup(reply_markup=weather_inl_btn())
    await call.answer()


@dp.callback_query(F.data.startswith('add_city'))
async def handle_add_city(call: types.CallbackQuery):
    try:
        _, city_name, telegram_id = call.data.split(":")  # Callback data format: add-city:<city_name>:<telegram_id>.
        print(f"{city_name}\n{telegram_id}")
        telegram_id = int(telegram_id)
        print(f"info: {call.data.split(":")}")

        result = db.add_city(city_name, telegram_id)
        if result:
            await call.answer(f"✅ {city_name} shahri muvaffaqiyatli saqlandi.", show_alert=True)
        else:
            await call.answer(f"❌ {city_name} shahrini saqlashda xatolik yuz berdi.", show_alert=True)

        await call.message.edit_text(text="Shaharlarni tanlang 👇")
        await call.message.edit_reply_markup(reply_markup=weather_inl_btn())
    except Exception as e:
        await call.message.answer(f"{e}\n/start /start /start /start")

@dp.callback_query(F.data == 'ortga_city2')
async def ortga_city2_func(call: CallbackQuery):
    await call.message.edit_text(text="🤖: Ortga qaytdingiz\nShaharlarni tanlang 👇")
    await call.message.edit_reply_markup(reply_markup=weather_inl_btn())


@dp.callback_query(F.data == 'ortga_city3')
async def ortga_city2_func(call: CallbackQuery):
    await call.message.edit_text(text="🤖: Ortga qaytdingiz\nShaharlarni tanlang 👇")
    await call.message.edit_reply_markup(reply_markup=weather_inl_btn())

@dp.callback_query(F.data == 'ortga1')
async def ortga_city2_func(call: CallbackQuery):
    await call.message.edit_text(text="🤖: Ortga qaytdingiz\nShaharlarni tanlang 👇")
    await call.message.edit_reply_markup(reply_markup=services_inline())
