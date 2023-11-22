from aiogram.fsm.state import State, StatesGroup


class CreateTicket(StatesGroup):
    title = State()


class ChangePassword(StatesGroup):
    current_password = State()
    new_password = State()
