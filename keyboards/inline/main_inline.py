from data.settings import *
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from data.database import db
from api.weather import get_weather_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

register_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Cheklovni olish 🔓", callback_data='register')
        ]
    ]
)

home_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Menu 🗃", callback_data="home_no")
        ]
    ]
)

home = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text="Botdan foydalanish 🗂", callback_data='services')],
        [InlineKeyboardButton(text="Malumotlarim 👤", callback_data='info')]
    ]
)

services_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ob-havo ⛅️", callback_data='weather')],
        [InlineKeyboardButton(text="Rasmlarga ishlov berish 🏞", callback_data='rembg')],
        [InlineKeyboardButton(text="Videolarga ishlov berish 📹", callback_data='video_not')],
        [InlineKeyboardButton(text="Suxbat qurish 💭", callback_data='live_chat')],
        [InlineKeyboardButton(text="Tarjima qilish (eng->uzs) 📖", callback_data='trans')],
        [InlineKeyboardButton(text="Wikipedia 📚", callback_data='wiki')],
        [InlineKeyboardButton(text="Ortga qaytish 🔙", callback_data='ortga1')],

    ]
)




class City_N(CallbackData, prefix='ikb'):
    city: str


weather_city = [
    'andijon',
    'buxoro',
    'fargona',
    'jizzax',
    'urganch',
    'namangan',
    'navoiy',
    'qashqadaryo',
    'samarqand',
    'sirdaryo',
    'surxondaryo',
    'toshkent'
]


def weather_inl_btn():
    btn = InlineKeyboardBuilder()
    for i in weather_city:
        btn.button(text=i.capitalize(), callback_data=City_N(city=i))
    btn.adjust(2)
    return btn.as_markup()


user_info_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ortga qaytish 🔙", callback_data='back_info')
        ],
        [InlineKeyboardButton(text="Ma'lumotlarni tahrirlash ✏️", callback_data='edit_info')],
        [
            InlineKeyboardButton(
                text="Primiumga obuna bulish ⭐️",
                callback_data='primium_info'
            )
        ]
    ]
)

is_primium = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Primiumga azo bulish", callback_data='is_prim'
            )
        ],
        [
            InlineKeyboardButton(
                text="Home 🔙", callback_data='is_prim_back'
            )
        ]
    ]
)

back_user_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Ortga qaytish 🔙", callback_data='back_info_us'
            )
        ]
    ]
)

gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="erkak", callback_data='male'),
            InlineKeyboardButton(text="Ayol", callback_data='female')
        ]
    ]
)

info_page_depozet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Hisobni to'ldirish", callback_data='depazet_info_page')
        ],
        [
            InlineKeyboardButton(
                text="Bosh Sahifa 📜", callback_data='home_info_page'
            )
        ]
    ]
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def delete_city_name(city_name: str, telegram_id: int) -> InlineKeyboardMarkup:
    btn = InlineKeyboardBuilder()
    btn.button(
        text="Ortga qaytish 🔙",
        callback_data="ortga_city2"
    )
    btn.button(
        text="❌ Shaharni o'chirish",
        callback_data=f"delete_city:{city_name}:{telegram_id}"
    )

    btn.adjust(1)
    return btn.as_markup()


def save_ciy_name(city_name: str, telegram_id: int) -> InlineKeyboardMarkup:
    btn = InlineKeyboardBuilder()
    btn.button(
        text="💾 Shaharni saqlash",
        callback_data=f'add_city:{city_name}:{telegram_id}'
    )
    btn.button(
        text="Ortga qaytish 🔙",
        callback_data='ortga_city3'
    )

    print(f"{city_name, telegram_id}")

    btn.adjust(1)
    return btn.as_markup()


primium_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash ✅", callback_data='yes_is')
        ],
        [
            InlineKeyboardButton(text="Bekor qilish ❌", callback_data='no_is')
        ]
    ]
)



admin_ = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Admin", url='https://t.me/hojibro')
        ]
    ]
)
