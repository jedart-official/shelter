# AIOGRAM IMPORTS
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class NumbersCallbackFactory(CallbackData, prefix="num_factory"):
    action: str
    value: Optional[int] = None
