from Models.Player import Player
from Models.Shelter import Shelter


class Session:
    all_turns: int = 4

    def __init__(self, session_id: int, db_id: int) -> None:
        self.id = session_id
        self.current_turn: int = 0
        self.players: list[Player] = list()
        self.keyboards: list[int] = list()
        self.players_dict: dict[int, Player] = dict()
        self.max_players: int = 0
        self.current_player: int = 0
        self.important_open: int = 2
        self.voiced_players: list[int] = list()
        self.players_to_voiced: dict[int, int] = dict()
        self.shelter: Shelter | None = None
        self.prepare_message_id: int | None = None
        self.db_id: int = db_id
        self.selected_chars: list[int] = list()

    def add_voiced_players(self, player_id: int, from_player: int) -> bool:
        self.voiced_players.append(player_id)
        if from_player in self.players_to_voiced:
            self.players_to_voiced[from_player] += 1
        else:
            self.players_to_voiced[from_player] = 1
        if len(self.voiced_players) == len(self.players):
            return False
        return True

    def create_shelter(self):
        self.shelter = Shelter(self.max_players)

    def update_players(self, new_array: list) -> None:
        self.players = new_array

    def set_max_players(self, number: int) -> None:
        self.max_players = number

    def inc_opened_characteristic(self) -> None:
        self.opened_characteristic += 1

    def inc_current_player(self) -> bool:
        if len(self.players) - 1 == self.current_player:
            return False
        else:
            self.current_player += 1
            return True

    def inc_current_turn(self) -> None:
        self.current_turn += 1

    def clear_opened_characteristic(self) -> None:
        self.opened_characteristic = 0

    def clear_current_player(self) -> None:
        self.current_player = 0

    def remove_char_from_player(self, player: int, index_of_char: int) -> None:
        self.players[player].characteristics.pop(index_of_char)
        self.players[player].characteristic_names.pop(index_of_char)

    def add_player_to_dict(self, player: Player) -> dict[int, Player]:
        self.players_dict[player.id] = player
        return self.players_dict

    def remove_player(self, key: int, index: int):
        del self.players_dict[key]
        self.players.pop(index)
