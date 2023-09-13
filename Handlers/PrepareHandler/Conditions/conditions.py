from aiogram.types import CallbackQuery
from Models import Player


def is_unreg_player(callback: CallbackQuery, all_players: dict[int, Player]) -> bool:
    return callback.from_user.id not in all_players


def is_full_party(all_players: dict, players_in_game: int) -> bool:
    return len(all_players) == players_in_game
