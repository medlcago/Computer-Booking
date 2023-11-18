from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline_utils import create_inline_keyboard
from states.users import CreateTicket
from utils.api_methods import TicketAPI

router = Router()


@router.callback_query(F.data == "ticket")
async def create_ticket(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    await call.message.answer(
        text="Для создания нового тикета, пожалуйста, опишите свою проблему или запрос ниже. Мы постарается вам помочь как можно скорее.\n\n"
             "Используй команду <i>/cancel</i>, если хочешь отменить это действие.",
    )
    await state.set_state(CreateTicket.title)


@router.message(CreateTicket.title)
async def create_ticket(message: Message, state: FSMContext, ticket_api: TicketAPI):
    await state.clear()
    title = message.text
    user_id = message.from_user.id
    if ticket := await ticket_api.create_ticket(
            title=title,
            assigned_to=user_id
    ):
        ticket_id = ticket.get("id")
        await message.reply(
            text=f"Тикет успешно создан.\nЕго уникальный идентификатор: <b>{ticket_id}</b>",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
