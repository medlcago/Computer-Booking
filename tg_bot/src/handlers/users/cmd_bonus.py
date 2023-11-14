import datetime

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.storage.redis import Redis
from aiogram.types import Message

from filters import IsPremium
from keyboards.inline_utils import create_inline_keyboard
from utils.api_methods import UserAPI

router = Router()


@router.message(Command(commands="bonus"), IsPremium())
async def command_bonus(message: Message, redis: Redis, user_api: UserAPI):
    user_id = message.from_user.id
    bonus = 10
    bonus_frequency = 48
    bonus_key = f"last_bonus_time:{user_id}"
    time_format = "%d.%m.%Y %H:%M:%S"
    last_bonus_time_str = await redis.get(name=bonus_key)
    last_bonus_time = datetime.datetime.strptime(last_bonus_time_str.decode(), time_format).replace(
        tzinfo=datetime.timezone.utc) if last_bonus_time_str else None

    current_time = datetime.datetime.now(datetime.timezone.utc)

    if last_bonus_time is None or (current_time - last_bonus_time) >= datetime.timedelta(hours=bonus_frequency):
        user = await user_api.get_user_by_id(user_id=user_id)
        if user:
            current_balance = user.get("balance")
            if await user_api.update_user_details(
                    user_id=user_id,
                    balance=current_balance + bonus
            ):
                await redis.set(
                    name=bonus_key,
                    value=current_time.strftime(time_format),
                    ex=bonus_frequency * 3600,
                    nx=True
                )
                await message.answer(
                    text=f"Вы получили бонус!\nНа ваш баланс начислено <b>{bonus} RUB</b>",
                    reply_markup=create_inline_keyboard(width=1, my_profile="👤 Мой профиль")
                )
            else:
                await message.answer(
                    text="Не удалось получить бонус :(",
                    reply_markup=create_inline_keyboard(width=1, my_profile="👤 Мой профиль")
                )
    else:
        next_bonus_time = (last_bonus_time + datetime.timedelta(hours=bonus_frequency)).strftime(time_format)
        await message.answer(
            text=f"Вы уже получили бонус.\nСледующий бонус будет доступен <b>{next_bonus_time} UTC+0</b>",
            reply_markup=create_inline_keyboard(width=1, my_profile="👤 Мой профиль")
        )


@router.message(Command(commands="bonus"))
async def command_bonus(message: Message):
    await message.reply("Команда доступна только обладателям подписки <b>Telegram Premium</b>")
