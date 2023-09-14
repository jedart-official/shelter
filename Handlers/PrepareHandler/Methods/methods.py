from aiogram.types import CallbackQuery
from Models.Player import Player
from Handlers.GameHandler.Methods.methods import turn
from Handlers.PrepareHandler.Messages.messages import send_start_game_message, send_history_message
from Models.Session import Session


def create_player(callback: CallbackQuery) -> Player:
    return Player(
        player_id=callback.from_user.id,
        player_name=callback.from_user.first_name,
        player_nickname=callback.from_user.username
    )


async def prepare_game(session: Session) -> None:
    active_users: list[Player] = list()
    local_keyboards: list[int] = list()
    for player_id, player in session.players_dict.items():
        active_users.append(player)
        local_keyboards.append(await send_start_game_message(player=player, group_id=session.id))
    session.keyboards = local_keyboards
    session.players = active_users


async def run_game_message(callback: CallbackQuery, session: Session) -> None:
    await send_history_message(callback=callback, shelter=session.shelter)
    await turn(session=session)
