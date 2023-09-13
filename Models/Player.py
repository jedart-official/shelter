# MORE IMPORTS
from Data.info import *
from Utils.helpers import generate_characteristic
import random


class Player:
    def __init__(self, player_id: int, player_name: str):
        self.id: int = player_id
        self.name: str = player_name
        self.gender: str = gender[random.randint(0, 1)]
        self.old: int = random.randint(18, 80)
        self.orientation: str = generate_characteristic(health)
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
            f"Пол: {self.gender}"
            f"\nВозраст: {self.old}"
            f"\nОриентация: {self.orientation}"
            f"\nТелосложение: {self.body}"
        )

    def set_characteristics(self):
        self.characteristics = [
            f"🧒 | *О человеке:*\n\n{self.create_person()}",
            f"❤️ | *Здоровье:*\n\n{self.health}",
            f"🎨 | *Хобби:*\n\n{self.hobby}",
            f"👻 | *Фобия:*\n\n{self.phobia}",
            f"😇 | *Характер:*\n\n{self.character}",
            f"📝 | *Доп.Информация:*\n\n{self.additional}",
            f"🧠 | *Знание:*\n\n{self.knowledge}",
            f"👜 | *Багаж:*\n\n{self.bag}",
        ]

    def send_info_about_player(self):
        # Set answer
        message_answer = f"" \
                         f"🧒ㅤ|ㅤ*О ВАС:*\n_{self.create_person()}_\n\n" \
                         f"❤️ㅤ|ㅤ*ЗДОРОВЬЕ*:️\n_{self.health}_\n\n" \
                         f"🎨ㅤ|ㅤ*ХОББИ:*\n_{self.hobby}_\n\n" \
                         f"👻ㅤ|ㅤ*ФОБИЯ:*\n_{self.phobia}_\n\n" \
                         f"😇ㅤ|ㅤ*ХАРАКТЕР:*\n_{self.character}_\n\n" \
                         f"📝ㅤ|ㅤ*ДОП.ИНФОРМАЦИЯ:*\n_{self.additional}_\n\n" \
                         f"🧠ㅤ|ㅤ*ЗНАНИЕ:*\n_{self.knowledge}_\n\n" \
                         f"👜ㅤ|ㅤ*БАГАЖ:*\n_{self.bag}_\n"
        return message_answer
