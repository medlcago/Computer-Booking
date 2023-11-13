from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from config import Config
from keyboards.callbackdata import TopUpBalance
from keyboards.inline_main import top_up_amount
from keyboards.inline_utils import create_inline_keyboard
from templates.texts import TOP_UP_BALANCE
from utils.api_methods import UserAPI, PaymentAPI

router = Router()


@router.callback_query(F.data == "top_up_balance")
async def top_up_balance(call: CallbackQuery):
    await call.message.edit_text(
        text=TOP_UP_BALANCE,
        reply_markup=top_up_amount()
    )


@router.callback_query(TopUpBalance.filter())
async def send_invoice(call: CallbackQuery, callback_data: TopUpBalance, bot: Bot, config: Config):
    await call.answer()
    amount = callback_data.amount

    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"Пополнение счета на {amount} рублей.",
        description=f"После оплаты на ваш счет поступит {amount} рублей.",
        payload=f"top_up_balance_{amount}rub_{call.from_user.id}",
        provider_token=config.tg.provider_token,
        currency="RUB",
        prices=[
            LabeledPrice(
                label="Пополнение счета",
                amount=amount * 100
            )
        ],
        start_parameter=str(call.from_user.id),
        protect_content=True,
        request_timeout=20
    )


@router.pre_checkout_query(F.invoice_payload.startswith("top_up_balance"))
async def pre_checkout_query(pre_checkout: PreCheckoutQuery, user_api: UserAPI, payment_api: PaymentAPI):
    user_id = pre_checkout.from_user.id
    amount = pre_checkout.total_amount // 100
    payload = pre_checkout.invoice_payload
    user = await user_api.get_user_by_id(user_id=user_id)
    if user:
        current_balance = user.get("balance")
        if await payment_api.create_payment(user_id=user_id, amount=amount, payload=payload):
            if await user_api.update_user_details(user_id=user_id, balance=current_balance + amount):
                await pre_checkout.answer(ok=True)
        else:
            await pre_checkout.answer(ok=False, error_message="Не удалось проверить платеж 😔")
    else:
        await pre_checkout.answer(ok=False, error_message="Не удалось проверить платеж 😔")


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    amount = message.successful_payment.total_amount // 100
    await message.answer(
        text=f"Спасибо! Получен платёж на сумму <b>{amount} {message.successful_payment.currency}</b>",
        reply_markup=create_inline_keyboard(
            width=1,
            my_profile="👤 Мой профиль",
            show_menu="Вернуться в меню")
    )
