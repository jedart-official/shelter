# AIOGRAM IMPORTS
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class MessageCallbackFactory(CallbackData, prefix="message_factory"):
    action: str
    group_id: Optional[int]
    value: Optional[int] = None
