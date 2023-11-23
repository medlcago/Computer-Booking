from aiogram.fsm.state import State, StatesGroup


class BlockUser(StatesGroup):
    user_id = State()


class UnBlockUser(StatesGroup):
    user_id = State()


class UserInfo(StatesGroup):
    user_id = State()


class UserBookingHistory(StatesGroup):
    user_id = State()


class UserPaymentHistory(StatesGroup):
    user_id = State()


class AddComputer(StatesGroup):
    computer_data = State()


class ComputerCategory(StatesGroup):
    category = State()


class DeleteComputer(StatesGroup):
    computer_id = State()


class ChangeBalance(StatesGroup):
    user_id = State()


class CloseTicket(StatesGroup):
    text = State()


class TicketInfo(StatesGroup):
    ticket_id = State()


class DeleteUser(StatesGroup):
    user_id = State()
