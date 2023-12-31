from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from utils.api_methods import UserAPI


class IsAdmin(Filter):
    async def __call__(self, event: Union[Message, CallbackQuery], user_api: UserAPI) -> bool:
        user = await user_api.get_user_by_id(user_id=event.from_user.id)
        if user:
            return user.get("is_admin")
