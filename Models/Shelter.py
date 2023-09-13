def set_voice_turn(players: int):
    shelter_voice = {1: 2, 2: 2, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1}
    return shelter_voice[players]


def set_players_in_shelter(players: int):
    shelter_players = {1: 1, 2: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 4, 9: 5}
    return shelter_players[players]


class Shelter:
    def __init__(self, max_players):
        self.players_in_shelter = set_players_in_shelter(max_players)
        self.voice_turn = set_voice_turn(max_players)
