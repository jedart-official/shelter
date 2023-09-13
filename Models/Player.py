# MORE IMPORTS
from Data.info import *
from Utils.helpers import generate_characteristic
import random


class Player:
    def __init__(self, player_id: int, player_name: str, player_nickname: str):
        self.id: int = player_id
        self.name: str = player_name
        self.nickname: str = player_nickname
        self.gender: str = gender[random.randint(0, 1)]
        self.job: str = generate_characteristic(jobs)
        self.old: int = random.randint(18, 80)
        self.orientation: str = generate_characteristic(orintation)
        self.body: str = generate_characteristic(body)
        self.health: str = generate_characteristic(health)
        self.hobby: str = generate_characteristic(hobby)
        self.phobia: str = generate_characteristic(phobia)
        self.character: str = generate_characteristic(character)
        self.additional: str = generate_characteristic(additional_info)
        self.bag: str = generate_characteristic(bag)
        self.knowledge: str = generate_characteristic(knowledge)
        self.characteristics: list = []
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
            f"🧒\t|\t*О человеке:*\n\n{self.create_person()}",
            f"❤️\t|\t*Здоровье:*\n\n|\t *{self.health}*",
            f"🎨\t|\t*Хобби:*\n\n|\t*{self.hobby}*",
            f"👻\t|\t*Фобия:*\n\n|\t*{self.phobia}*",
            f"😇\t|\t*Характер:*\n\n|\t*{self.character}*",
            f"📝\t|\t*Доп.Информация:*\n\n|\t*{self.additional}*",
            f"🧠\t|\t*Знание:*\n\n|\t*{self.knowledge}*",
            f"👜\t|\t*Багаж:*\n\n|\t*{self.bag}*",
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
