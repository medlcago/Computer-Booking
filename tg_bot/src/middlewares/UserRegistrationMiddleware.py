from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from keyboards.reply_main import get_phone_keyboard
from utils.api_methods.users import UserAPI
from utils.misc import generate_user_password


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_contact = get_flag(data, "user_contact")
        user_api: UserAPI = data.get("user_api")
        check_user = await user_api.get_user_by_id(user_id=event.from_user.id)

        if user_contact is None:
            if check_user:
                return await handler(event, data)
            else:
                await event.answer("""🗂 <b>Номер телефона</b>

Вам необходимо подтвердить номер телефона для того, чтобы завершить идентификацию.

<b>Для этого нажмите кнопку ниже.</b>""", reply_markup=get_phone_keyboard())

        if user_contact and not check_user:
            user_password: str = generate_user_password()
            user: dict = await user_api.create_user(
                user_id=event.from_user.id,
                fullname=event.from_user.full_name,
                username=event.from_user.username,
                password=user_password,
                phone_number=event.contact.phone_number
            )
            if user:
                data["user_password"] = user_password
                return await handler(event, data)
            else:
                await event.answer("Произошла <b>ошибка</b> при регистрации. Пожалуйста, повторите попытку.")
