from aiogram import types, Router, F

from keyboards.inline_main import main_menu

router = Router()


@router.callback_query(F.data == "show_menu")
async def show_main_menu(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Добро пожаловать 😽\n"
             "Это основное меню. Здесь ты можешь выбрать нужное тебе действие)",
        reply_markup=main_menu()
    )
