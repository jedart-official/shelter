# MORE IMPORTS
import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from config import bot, storage


async def get_group_context(chat_id: int) -> FSMContext:
    storage_key = StorageKey(chat_id=chat_id, bot_id=bot.id, user_id=chat_id)
    context = FSMContext(key=storage_key, storage=storage)
    return context


def generate_characteristic(array) -> str:
    """
    :rtype: object
    :param array: 
    :return: 
    """
    return array[random.randint(0, len(array) - 1)]


def create_characteristics_array(player) -> object:
    """
    :rtype: object
    :return: 
    """
    person = (
        f"Пол: {player.gender}"
        f"\nВозраст: {player.old}"
        f"\nОриентация: {player.orientation}"
        f"\nТелосложение: {player.body}"
    )
    characteristics = list()
    characteristics.append(f"*О человеке:* {person}")
    characteristics.append(f"*Здоровье:* {player.health}")
    characteristics.append(f"*Хобби:*{player.hobby}")
    characteristics.append(f"Характер: {player.character}")
    characteristics.append(f"Фобия: {player.phobia}")
    characteristics.append(f"Доп.Информация: {player.additional}")
    characteristics.append(f"Знание: {player.knowledge}")
    characteristics.append(f"Багаж{player.bag}")
    return characteristics


def create_characteristic_names_array():
    """

    :return: 
    """
    characteristic_names = list()
    characteristic_names.append("Обо мне")
    characteristic_names.append("Здоровье")
    characteristic_names.append("Хобби")
    characteristic_names.append("Характер")
    characteristic_names.append("Фобия")
    characteristic_names.append("Доп.информация")
    characteristic_names.append("Знание")
    characteristic_names.append("Багаж")
    return characteristic_names
