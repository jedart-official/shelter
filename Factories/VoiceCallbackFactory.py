# AIOGRAM IMPORTS
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class VoiceCallbackFactory(CallbackData, prefix="voice_factory"):
    action: str
    value: Optional[int] = None
