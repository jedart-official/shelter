# MORE IMPORTS
from aiogram.types import Message
from Data.info import *
from Utils.helpers import get_random_item_from_array
import random


class Player:
    def __init__(self, player_id: int, player_name: str, player_nickname: str):
        self.id: int = player_id
        self.name: str = player_name
        self.nickname: str = player_nickname
        self.gender: str = gender[random.randint(0, 1)]
        self.job: str = get_random_item_from_array(jobs)
        self.old: int = random.randint(18, 80)
        self.orientation: str = get_random_item_from_array(orintation)
        self.body: str = get_random_item_from_array(body)
        self.health: str = get_random_item_from_array(health)
        self.hobby: str = get_random_item_from_array(hobby)
        self.phobia: str = get_random_item_from_array(phobia)
        self.character: str = get_random_item_from_array(character)
        self.additional: str = get_random_item_from_array(additional_info)
        self.bag: str = get_random_item_from_array(bag)
        self.knowledge: str = get_random_item_from_array(knowledge)
        self.characteristics: list = []
        self.chars_message: str = ''
        self.characteristic_names: list = [
            "Обо мне", "Здоровье", "Хобби", "Фобия",
            "Характер", "Доп.информация", "Знание", "Багаж"
        ]
        self.set_characteristics()

    def create_person(self):
        return (
            f"Пол\t|\t*{self.gender}*"
            f"\nВозраст\t|\t*{self.old}*"
            f"\nОриентация\t|\t *{self.orientation}*"
            f"\nТелосложение\t|\t*{self.body}*"
        )

    def set_characteristics(self):
        self.characteristics = [
            f"🧒\t|\t*О ЧЕЛОВЕКЕ:*\n{self.create_person()}",
            f"❤️\t|\t*ЗДОРОВЬЕ:*\n|\t *{self.health}*",
            f"🎨\t|\t*ХОББИ:*\n|\t*{self.hobby}*",
            f"👻\t|\t*ФОБИЯ:*\n|\t*{self.phobia}*",
            f"😇\t|\t*ХАРАКТЕР:*\n|\t*{self.character}*",
            f"📝\t|\t*ДОП.ИНФОРМАЦИЯ:*\n|\t*{self.additional}*",
            f"🧠\t|\t*ЗНАНИЕ:*\n|\t*{self.knowledge}*",
            f"👜\t|\t*БАГАЖ:*\n|\t*{self.bag}*",
        ]

    def send_info_about_player(self):
        # Set answer
        message_answer = f"" \
                         f"🧒\t|\t*О ВАС:*\n_{self.create_person()}_\n\n" \
                         f"❤️\t|\t*ЗДОРОВЬЕ*:️\n_{self.health}_\n\n" \
                         f"🎨\t|\t*ХОББИ:*\n_{self.hobby}_\n\n" \
                         f"👻\t|\t*ФОБИЯ:*\n_{self.phobia}_\n\n" \
                         f"😇\t|\t*ХАРАКТЕР:*\n_{self.character}_\n\n" \
                         f"📝\t|\t*ДОП.ИНФОРМАЦИЯ:*\n_{self.additional}_\n\n" \
                         f"🧠\t|\t*ЗНАНИЕ:*\n_{self.knowledge}_\n\n" \
                         f"👜\t|\t*БАГАЖ:*\n_{self.bag}_\n"
        return message_answer


def create_player(message: Message) -> Player:
    return Player(
        player_id=message.from_user.id,
        player_name=message.from_user.first_name,
        player_nickname=message.from_user.username
    )
