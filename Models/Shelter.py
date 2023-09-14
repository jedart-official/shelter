from random import randint

from Data.info import disasters, shelter_info
from Utils.helpers import generate_characteristic


def set_voice_turn(players: int):
    shelter_voice = {1: 2, 2: 1, 3: 1, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1}
    return shelter_voice[players]


def set_players_in_shelter(players: int):
    shelter_players = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 4, 9: 5}
    return shelter_players[players]


def set_time_to_live():
    time_list: list[str] = ['месяцев', 'лет / года']
    time_char = randint(0, 1)
    return f"{randint(1, 12)} {time_list[time_char]}"


def set_shelter_info() -> dict:
    shelter_type: str = shelter_info['type']
    shelter_main_room: str = shelter_info['main_room']
    shelter_additional_room: str = shelter_info['additional_room']
    shelter_state: str = shelter_info['state']
    shelter_invertory: str = shelter_info['invertory']
    shelter_location: str = shelter_info['location']
    return {
        'type': generate_characteristic(shelter_type),
        'state': generate_characteristic(shelter_state),
        'main_room': generate_characteristic(shelter_main_room),
        'additional_room': generate_characteristic(shelter_additional_room),
        'location': generate_characteristic(shelter_location),
        'invertory': generate_characteristic(shelter_invertory),
    }


class Shelter:
    def __init__(self, max_players):
        self.players_in_shelter = set_players_in_shelter(max_players)
        self.voice_turn = set_voice_turn(max_players)
        self.history = generate_characteristic(disasters)
        self.live_time = set_time_to_live()
        self.shelter_info = set_shelter_info()
