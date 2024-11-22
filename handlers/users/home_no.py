import asyncio
from pyexpat.errors import messages
from aiogram.fsm.context import FSMContext
from data.settings import *
from aiogram import types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from data.database import db
from keyboards.inline.main_inline import *
from states.state import RegistrForm
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove


@dp.callback_query(F.data == 'home_no')
async def no_register(call: CallbackQuery):
    await call.answer(text="Access to the Services is limited 🔐", cache_time=60)
    await call.message.edit_text(text="<b>Xizmatlarga kirish cheklangan 🔐</b>", )
    await call.message.edit_reply_markup(reply_markup=register_inline)


@dp.callback_query(F.data == "register")
async def register_func(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer(text="Process started")
        await state.set_state(RegistrForm.first_name)
        await call.message.edit_text(text="<b>Ismingizni kiriting \n <i>Masalan: Shahzod</i></b>")
        await call.message.edit_reply_markup(reply_markup=None)

    except:
        pass

@dp.message(RegistrForm.first_name)
async def first_name_func(msg: Message, state: FSMContext):
    if len(msg.text.strip()) < 3:
        await msg.answer(f"<b>Ismingiz kamida 4 ta belgidan iborat bo‘lishi kerak. 😊  </b>")
    else:
        await state.set_state(RegistrForm.last_name)
        await state.update_data(first_name=msg.text)
        await msg.answer(f"<b>Fameliyangizni kiriting \n"
                         f"</b><i>Masalan: Omonov</i>")


@dp.message(RegistrForm.last_name)
async def last_name_func(msg: Message, state: FSMContext):
    if len(msg.text.strip()) <= 4:
        await msg.answer(f"<b>Fameliya kamida 4 ta belgidan iborat bo‘lishi kerak. 😊  </b>")
    else:
        await state.set_state(RegistrForm.gender)
        await state.update_data(last_name=msg.text)
        await msg.answer(f"Tanlang 👆", reply_markup=gender)


@dp.callback_query(F.data == 'male')
async def gender_func(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer(text="Gender is selected")
        ok = await call.message.answer(text="cheklov olinmoqda...")
        await asyncio.sleep(2)
        await ok.delete()
        await state.update_data(gender='erkak')

        user_data = await state.get_data()

        if 'first_name' not in user_data or 'last_name' not in user_data or 'gender' not in user_data:
            await call.message.answer(text="Ma'lumotlar to'liq emas, qayta urinib ko'ring!")
            return

        db.update_user_data(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            gender=user_data['gender'],
            telegram_id=call.from_user.id
        )


        # await call.message.edit_reply_markup(reply_markup=None)
        await call.message.edit_text(text="Bosh Sahifa 📜")
        await call.message.edit_reply_markup(reply_markup=home)
    except Exception as e:
        await call.message.answer(text=f"Xato yuz berdi: {e}")




@dp.callback_query(F.data == 'female')
async def gender_func_fe(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer(text="Gender is selected")
        ok = await call.message.answer(text="cheklov olinmoqda...")
        await asyncio.sleep(2)
        await ok.delete()
        await state.update_data(gender='erkak')

        user_data = await state.get_data()

        if 'first_name' not in user_data or 'last_name' not in user_data or 'gender' not in user_data:
            await call.message.answer(text="Ma'lumotlar to'liq emas, qayta urinib ko'ring!")
            return

        db.update_user_data(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            gender=user_data['gender'],
            telegram_id=call.from_user.id
        )


        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(text="Bosh Sahifa 📜", reply_markup=home)
    except Exception as e:
        await call.message.answer(text=f"Xato yuz berdi: {e}")




@dp.callback_query(F.data == 'balance')
async def back_info_fumc(call:CallbackQuery):
    await call.answer(text="Sozlanmoqda ⚙️", show_alert=True)


