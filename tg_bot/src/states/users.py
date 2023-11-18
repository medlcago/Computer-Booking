from aiogram.fsm.state import State, StatesGroup


class CreateTicket(StatesGroup):
    title = State()
