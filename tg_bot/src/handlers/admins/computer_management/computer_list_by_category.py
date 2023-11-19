from datetime import datetime
from datetime import timezone

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline_utils import create_inline_keyboard
from states.admins import ComputerCategory
from utils.api_methods import ComputerAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "computer_list_by_category_excel")
async def computer_list_by_category_excel(call: CallbackQuery, state: FSMContext):
    """
    Список компьютеров конкретной категории в формате Excel (1)
    """
    await call.answer(cache_time=15)
    sent_message = await call.message.answer(
        text="Вы хотите получить список компьютеров конкретной категории.\n"
             "Пожалуйста, введите категорию (VIP или Regular)"
    )
    await state.set_state(ComputerCategory.category)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(ComputerCategory.category, F.text.in_({"VIP", "Regular"}))
async def computer_list_by_category_excel(message: Message, bot: Bot, state: FSMContext, computer_api: ComputerAPI):
    """
    Список компьютеров конкретной категории в формате Excel (2)
    """
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    category = message.text
    computers: list[dict] = await computer_api.get_computers_by_category(category=category)

    if computers:
        headers = list(computers[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=computers, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + f"_computer_{category}_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await message.reply_document(
            document=file,
            caption=f"Список компьютеров категории <i>{category}</i>",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await message.reply(f"Не удалось получить информацию о компьютерах категории <i>{category}</i>")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
