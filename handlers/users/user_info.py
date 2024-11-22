import asyncio
from aiogram.fsm.context import FSMContext
from data.settings import *
from aiogram import F
from aiogram.types import Message, CallbackQuery
from data.database import db
from keyboards.inline.main_inline import *
from states.state import RegistrForm2


@dp.callback_query(F.data == 'info')
async def user_info(call: CallbackQuery):
    telegram_id = call.from_user.id
    user_data = db.sql_check_user(telegram_id=telegram_id)
    await call.answer(text="Your information")
    primium = int(user_data['primium'])
    if primium == 1:
        result = 'Obuna bulingan'
    else:
        result = 'Obuna bulinmagan'
    await call.message.edit_text(text=f"<b>🤖: Sizning ma'lumotlaringiz 📃\n"
                                      f"👤 User id: <code>{user_data['id']}</code></b>\n"
                                      f"🆔 Telegram id: <code>{user_data['telegram_id']}</code>\n"
                                      f"📝 Telegram full name: <code>{user_data['telegram_full_name']}</code>\n"
                                      f"👤 Full name: <code>{user_data['first_name']} {user_data['last_name']}</code>\n"
                                      f"👤 Gender: <code>{user_data['gender']}</code>\n"
                                      f"⭐️ Primium: <code>{result}</code>\n"
                                      f"💸 Balance: <code>{user_data['balance']}</code>")
    await call.message.edit_reply_markup(reply_markup=user_info_inline)


@dp.callback_query(F.data == 'edit_info')
async def back_info_fumc(call: CallbackQuery, state: FSMContext):
    await call.answer(text='edit profile page')
    user_data = db.sql_check_user(telegram_id=call.from_user.id)
    balanc = str(user_data.get('balance'))
    if balanc == '1':
        try:
            await call.answer(text="Process started")
            await state.set_state(RegistrForm2.first_name)
            await call.message.edit_text(text="<b>Ismingizni kiriting \n <i>Masalan: Shahzod</i></b>")
        except:
            pass
    else:
        await call.message.answer(
            "🤖<b>: Ma'lumotlarni uzgartirish uchun siz primiumga obuna bulgan bulishiz kerak 😞</b>",
            reply_markup=is_primium)


@dp.message(RegistrForm2.first_name)
async def first_name_func(msg: Message, state: FSMContext):
    if len(msg.text.strip()) < 3:
        await msg.answer(f"<b>Ismingiz kamida 4 ta belgidan iborat bo‘lishi kerak. 😊  </b>")
    else:
        await state.set_state(RegistrForm2.last_name)
        await state.update_data(first_name=msg.text)
        await msg.answer(f"<b>Fameliyangizni kiriting \n"
                         f"</b><i>Masalan: Omonov</i>")


@dp.message(RegistrForm2.last_name)
async def last_name_func(msg: Message, state: FSMContext):
    if len(msg.text.strip()) <= 4:
        await msg.answer(f"<b>Fameliya kamida 4 ta belgidan iborat bo‘lishi kerak. 😊  </b>")
    else:
        await state.set_state(RegistrForm2.gender)
        await state.update_data(last_name=msg.text)
        await msg.answer(f"Tanlang 👇", reply_markup=gender)


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


@dp.callback_query(F.data == 'is_prim')
async def back_info_fumc(call: CallbackQuery):
    user_first_name = db.user_info(telegram_id=call.from_user.id)
    await call.answer(f"Is primium buy page")
    await call.message.edit_text(f"🤖<b>: {user_first_name.get('first_name')} primium narxi 3900 som\n"
                                 f"Sotib olishni hohlaysizmi</b>")
    await call.message.edit_reply_markup(reply_markup=primium_yes_no)


@dp.callback_query(F.data == 'yes_is')
async def back_info_func(call: CallbackQuery):
    await call.answer(text='Primium page')
    user_data = db.user_info(telegram_id=call.from_user.id)
    balance = user_data.get('balance')

    if balance is not None:
        balance = int(balance)

        # Agar foydalanuvchi primiumga obuna bo'lmagan bo'lsa
        if user_data.get('primium') == 0:
            if balance >= 3900:
                # Foydalanuvchidan mablag'ni kamaytirish
                db.update_user_balance(
                    balance=balance - 3900,
                    telegram_id=call.from_user.id
                )

                # Primium holatini yangilash
                db.is_primium(
                    primium=1,
                    telegram_id=call.from_user.id
                )

                # Muvaffaqiyatli primium xabari
                await call.message.edit_text(
                    text="<b>Siz primiumga obuna bo'ldingiz ⭐️</b>"
                )
                await call.message.edit_reply_markup(reply_markup=back_user_info)
            else:
                # Yetarli mablag' mavjud emasligi
                await call.message.edit_text(
                    text="🤖<b>: Balansingizda mablag yetarli emas 💸😞</b>"
                )
                await call.message.edit_reply_markup(reply_markup=info_page_depozet)
        else:
            # Foydalanuvchi allaqachon primiumga obuna bo'lgan
            await call.message.edit_text(
                text="Siz allaqachon primiumga azo bo'lgansiz ⭐️"
            )
            await call.message.edit_reply_markup(reply_markup=home)
    else:
        # Agar foydalanuvchi balans topilmasa
        await call.message.edit_text("Xato yuz berdi, iltimos keyinroq urinib ko'ring!")



@dp.callback_query(F.data == 'no_is')
async def back_info_fumc(call: CallbackQuery):
    await call.answer(text='primium page')
    await call.message.edit_text(text=f"Ortga qaytdingiz")
    await call.message.edit_reply_markup(reply_markup=home)


@dp.callback_query(F.data == 'primium_info')
async def back_info_fumc(call: CallbackQuery):
    await call.answer(text='primium page')
    user_data = db.user_info(telegram_id=call.from_user.id)
    balanc = int(user_data['balance'])
    if balanc >= 3900:
        db.update_user_balance(
            balance=balanc - 3900,
            telegram_id=call.from_user.id
        )
        await call.message.edit_text(text="<b>Siz primiumga obuna buldingiz ⭐️</b>", reply_markup=back_user_info)
        await call.message.edit_reply_markup(reply_markup=back_user_info)
    else:
        await call.message.edit_text("🤖<b>: Balansingizda mablag yetarli emas 💸😞</b>")
        await call.message.edit_reply_markup(reply_markup=info_page_depozet)


@dp.callback_query(F.data == 'home_info_page')
async def back_info_fumc(call: CallbackQuery):
    try:
        await call.answer(text='Home page')
        await call.message.edit_text(text="Bosh Sahifa 📜")
        await call.message.edit_reply_markup(reply_markup=home)
    except:
        pass


@dp.callback_query(F.data == 'is_prim_back')
async def back_info_fumc(call: CallbackQuery):
    try:
        await call.answer(text='Home page')
        await call.message.edit_text(text="Bosh Sahifa 📜")
        await call.message.edit_reply_markup(reply_markup=user_info_inline)
    except:
        pass


@dp.callback_query(F.data == 'back_info_us')
async def back_info_fumc(call: CallbackQuery):
    try:
        await call.answer(text='Home page')
        await call.message.edit_text(text="Bosh Sahifa 📜")
        await call.message.edit_reply_markup(reply_markup=user_info_inline)
    except:
        pass


@dp.callback_query(F.data == 'back_info')
async def back_info_fumc(call: CallbackQuery):
    try:
        await call.answer(text='Home page')
        await call.message.edit_text(text="Bosh Sahifa 📜")
        await call.message.edit_reply_markup(reply_markup=home)
    except:
        pass
