from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, CallbackQuery

from keyboards.inline_utils import create_inline_keyboard
from utils.api_methods import UserAPI


class BlockMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        user_api: UserAPI = data["user_api"]
        skip_flag = get_flag(data, "skip")
        if skip_flag or await self.is_allowed(user_id=user_id, user_api=user_api):
            return await handler(event, data)
        await self.handle_restriction(event)

    @staticmethod
    async def is_allowed(user_id: int, user_api: UserAPI) -> bool:
        user = await user_api.get_user_by_id(user_id=user_id)
        return not user.get("is_blocked")

    @staticmethod
    async def handle_restriction(event: Union[Message, CallbackQuery]) -> None:
        close_button = create_inline_keyboard(width=1, close="❌ Закрыть")
        if isinstance(event, CallbackQuery):
            await event.answer("ACCESS_DENIED")
            await event.message.answer(
                text="<b>Access denied.\n"
                     "You have been blocked for violating the rules.</b>",
                reply_markup=close_button
            )
        else:
            await event.answer(
                text="<b>Access denied.\n"
                     "You have been blocked for violating the rules.</b>",
                reply_markup=close_button
            )
