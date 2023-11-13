from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.admins import DeleteComputer
from utils.api_methods import ComputerAPI

router = Router()


@router.callback_query(F.data == "delete_computer")
async def delete_computer(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    await call.message.answer("Вы хотите удалить компьютер.\nПожалуйста, введите его ID")
    await state.set_state(DeleteComputer.computer_id)


@router.message(DeleteComputer.computer_id)
async def delete_computer(message: Message, state: FSMContext, computer_api: ComputerAPI):
    await state.clear()
    try:
        computer_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID компьютера</i> должен быть целым числом!")
        return

    if await computer_api.delete_computer(computer_id=computer_id):
        await message.reply("Компьютер был успешно удален!")
    else:
        await message.reply("Не удалось удалить компьютер!")
