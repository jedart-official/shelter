from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from States.main import get_session
from Models.Player import Player
from Handlers.GameHandler.Conditions.conditions import is_session
from Handlers.GameHandler.Methods.methods import turn
from Handlers.PrepareHandler.Messages.messages import send_start_game_message, send_run_game_message
from Models.Session import Session


def create_player(callback: CallbackQuery) -> Player:
    return Player(player_id=callback.from_user.id,
                  player_name=callback.from_user.first_name)


async def prepare_game(state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    active_users: list[Player] = list()
    for player_id, player in session.players_dict.items():
        active_users.append(player)
        await send_start_game_message(player=player, group_id=session.id)

    if await is_session(state=state):
        session.players = active_users


async def run_game_message(callback: CallbackQuery, state: FSMContext) -> None:
    await send_run_game_message(callback=callback)
    await turn(state=state)
