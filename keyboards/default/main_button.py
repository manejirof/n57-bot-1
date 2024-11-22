from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

buton = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="👍"
            )
        ],
        [
            KeyboardButton(
                text="👎"
            )
        ],
    ]
)

