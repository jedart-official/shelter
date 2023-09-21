# MORE IMPORTS
import random

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from Database.main import session_db, MessageDB, SessionDB
from config import bot, storage


async def get_group_context(chat_id: int) -> FSMContext:
    """
    Get group context when request from private chat
    :param chat_id:
    :return: FSMContext
    """
    storage_key = StorageKey(chat_id=chat_id, bot_id=bot.id, user_id=chat_id)
    context = FSMContext(key=storage_key, storage=storage)
    return context


def get_random_item_from_array(array) -> str | None:
    """
    Get a random item from a list
    :rtype: object
    :param array: 
    :return: Str | None
    """
    return array[random.randint(0, len(array) - 1)]


async def is_session(state: FSMContext | None) -> bool:
    """
    Checks if there is a session in the chat room
    :param state:
    :return: Bool
    """
    if type(state) is None:
        return False
    session_data = await state.get_data()
    return 'session' in session_data


async def clear_group_messages(chat_id: int, session_id: int) -> None:
    """
    Deleting all messages created during the session
    :param chat_id:
    :param session_id:
    """
    access = await bot.get_chat_member(chat_id=chat_id, user_id=bot.id)
    if access.status == 'administrator':
        messages = session_db.query(MessageDB).filter(MessageDB.chat_id == chat_id)
        for message in messages:
            try:
                await bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
            except TelegramBadRequest:
                continue
        session = session_db.query(SessionDB).get(session_id)
        session_db.delete(session)
        session_db.commit()
    else:
        bot.send_message(chat_id=chat_id,
                         text='Для праавильной работы бота, ему требуются права администратора в группе')



