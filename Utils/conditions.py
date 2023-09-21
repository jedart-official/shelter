from aiogram.types import CallbackQuery

from Models import Player, Session
from Models.Shelter import Shelter


def is_unregistered_player(user_id, all_players: dict[int, Player]) -> bool:
    return user_id not in all_players


def is_full_party(all_players: dict, players_in_game: int) -> bool:
    return len(all_players) == players_in_game


def is_current_user_keyboard(message_id: int, keywords: list[int]):
    return message_id in keywords


def is_current_player(callback: CallbackQuery, session: Session) -> bool:
    from_user = callback.from_user.id
    current_session_player: Player = session.players_dict[session.current_player]
    current_session_player_id: int = current_session_player.id
    return from_user == current_session_player_id


def is_finish(session: Session) -> bool:
    shelter: Shelter = session.shelter
    return len(session.players_dict) == shelter.players_in_shelter


def is_free_characteristic(session: Session) -> bool | str:
    selected: int = len(session.selected_chars)
    important: int = session.important_open
    return selected == important


def is_player(session: Session, voiced_player_id: int):
    return voiced_player_id in session.players_dict


def is_voice_turn(session: Session) -> bool:
    shelter: Shelter = session.shelter
    return session.current_turn >= shelter.voice_turn
