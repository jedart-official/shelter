import asyncio

from aiogram.types import CallbackQuery, Message

from Factories.MessageCallbackFactory import MessageCallbackFactory
from Handlers.ProcessHandler.Messages.messages import send_information_message, \
    send_edit_keyboard_of_char, send_turn_message, send_player_turn_message, send_start_meeting_message, \
    send_kicked_message, send_finished_message, send_to_player_turn_message, send_history_message, \
    send_start_game_message
from Models.Session import Session
from Models.Shelter import Shelter
from States.main import clear_session
from Utils.conditions import is_free_characteristic, is_voice_turn, is_finish


async def start_game_manager(session: Session):
    await run_game_message(session=session)
    await turn(session=session)
    await player_turn_message(session=session)


async def set_game_info(session: Session):
    session.shelter = Shelter(max_players=len(session.players_dict))
    local_keyboards: list[int] = list(await asyncio.gather(
        *[send_start_game_message(player=player, group_id=session.id) for player in session.players_dict.values()]
    ))
    session.keyboards = local_keyboards


async def run_game_message(session: Session) -> None:
    await send_history_message(chat_id=session.id, shelter=session.shelter, session_db_id=session.db_id)
    await set_game_info(session=session)


async def turn(session: Session) -> None:
    session.opened_characteristic = 0
    session.current_turn += 1
    await asyncio.sleep(1)
    await send_turn_message(
        chat_id=session.id,
        current_turn=session.current_turn,
        session_db_id=session.db_id
    )


async def player_turn_message(session: Session) -> None:
    session.opened_characteristic = 0
    await send_player_turn_message(session=session)
    await send_to_player_turn_message(
        chars_count=session.important_open,
        current_player=session.players_dict[session.current_player]
    )


async def prepare_char_message(session: Session, value: int, message_id: int):
    current_player = session.players_dict[session.current_player]
    current_player.chars_message += f"{current_player.characteristics[value]}\n\n"
    session.remove_char_from_player(player=session.current_player, index_of_char=value)
    await send_edit_keyboard_of_char(
        message_id=message_id,
        session=session,
        group_id=session.id
    )


async def check_free_characteristics(callback: CallbackQuery, callback_data: MessageCallbackFactory, session: Session):
    session.selected_chars.append(callback_data.value)
    await prepare_char_message(session=session, value=callback_data.value, message_id=callback.message.message_id)
    if is_free_characteristic(session=session):
        await turn_of_player(session=session)
        await is_incremented_player(session=session)
        session.selected_chars = list()


async def is_incremented_player(session: Session):
    if session.inc_current_player():
        await player_turn_message(session=session)
    else:
        await voice_turn(session=session)


async def voice_turn(session: Session):
    if is_voice_turn(session=session):
        await send_start_meeting_message(session=session)
    else:
        await turn(session=session)


async def turn_of_player(session: Session) -> None:
    await send_information_message(session=session)


def find_kicked_player(session: Session) -> str:
    players_to_voiced: dict[int, int] = session.players_to_voiced
    kicked_player_id: int = max(players_to_voiced, key=players_to_voiced.get)
    player_nickname: str = next(
        (player.name for player in session.players_dict.values() if player.id == kicked_player_id), '')
    session.remove_player(key=kicked_player_id)
    return player_nickname


async def send_kicked_player(session: Session, message: Message):
    await send_kicked_message(
        player_name=find_kicked_player(session=session),
        chat_id=session.id,
        session_db_id=session.db_id
    )
    if is_finish(session=session):
        await send_finished_message(chat_id=session.id, players=list(session.players_dict.values()))
        await clear_session(message=message)
    else:
        await turn(session=session)
