import logging

from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from utils.api_methods import UserAPI

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated, user_api: UserAPI):
    logging.info(f"Пользователь {event.from_user.id} заблокировал бота.")
    await user_api.update_user_details(
        user_id=event.from_user.id,
        is_active=False
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated, user_api: UserAPI):
    logging.info(f"Пользователь {event.from_user.id} разблокировал бота.")
    await user_api.update_user_details(
        user_id=event.from_user.id,
        is_active=True
    )
