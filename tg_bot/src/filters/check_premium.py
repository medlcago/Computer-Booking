from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery


class IsPremium(Filter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        return event.from_user.is_premium
