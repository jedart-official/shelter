from Models.Player import Player
from Models.Shelter import Shelter


class Session:
    def __init__(self, session_id: int, db_id: int) -> None:
        self.id = session_id
        self.current_turn: int = 0
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
        if len(self.voiced_players) == len(self.players_dict):
            return False
        return True

    def inc_current_player(self) -> bool:
        players_indexes = list(self.players_dict.keys())
        try:
            next_player = players_indexes.index(self.current_player)
            self.current_player = players_indexes[next_player + 1]
            return True
        except IndexError:
            return False

    def remove_char_from_player(self, player: int, index_of_char: int) -> None:
        self.players_dict[player].characteristics.pop(index_of_char)
        self.players_dict[player].characteristic_names.pop(index_of_char)

    def remove_player(self, key: int):
        del self.players_dict[key]


