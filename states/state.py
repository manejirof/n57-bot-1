from aiogram.fsm.state import State, StatesGroup


class RegistrForm(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()


class RegistrForm2(StatesGroup):
    first_name = State()
    last_name = State()
    gender = State()