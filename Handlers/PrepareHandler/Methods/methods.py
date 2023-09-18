from aiogram.types import Message
from Models.Player import Player, create_player
from Handlers.ProcessHandler.Methods.methods import turn
from Handlers.PrepareHandler.Messages.messages import send_start_game_message, send_history_message, \
    delete_prepare_message, send_prepare_message
from Models.Session import Session
from Utils.conditions import is_full_party


async def prepare_game(session: Session) -> None:
    active_users: list[Player] = list()
    for player_id, player in session.players_dict.items():
        active_users.append(player)
    session.players = active_users


async def run_game_message(session: Session) -> None:
    await send_history_message(chat_id=session.id, shelter=session.shelter, session_db_id=session.db_id)
    local_keyboards: list[int] = list()
    for player in session.players:
        local_keyboards.append(await send_start_game_message(player=player, group_id=session.id))
    session.keyboards = local_keyboards
    await turn(session=session)


async def add_player(message: Message, session: Session) -> None:
    all_players: dict[int, Player] = session.players_dict
    all_players[message.from_user.id] = create_player(message=message)
    if is_full_party(all_players=all_players, players_in_game=session.max_players):
        await delete_prepare_message(chat_id=session.id, message_id=session.prepare_message_id)
        await prepare_game(session=session)
        await run_game_message(session=session)
    else:
        await send_prepare_message(session=session, all_players=session.players_dict,
                                   max_players=session.max_players)
