from aiogram.types import Message


def is_chat_group(message: Message) -> bool:
    return message.chat.type == "group"
