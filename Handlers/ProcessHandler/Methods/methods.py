from aiogram.types import CallbackQuery, Message
from Factories.MessageCallbackFactory import MessageCallbackFactory
from Handlers.ProcessHandler.Messages.messages import send_information_message, \
    send_edit_keyboard_of_char, send_turn_message, send_player_turn_message, send_start_meeting_message, \
    send_kicked_message, send_finished_message, send_to_player_turn_message
from Handlers.StartHandler.Methods.methods import clear_session
from Models.Session import Session
from Utils.conditions import is_free_characteristic, is_voice_turn, is_finish


async def turn(session: Session) -> None:
    session.opened_characteristic = 0
    session.current_player = 0
    session.current_turn += 1
    await send_turn_message(chat_id=session.id, current_turn=session.current_turn, session_db_id=session.db_id)
    await player_turn_message(session=session)


async def player_turn_message(session: Session) -> None:
    session.opened_characteristic = 0
    await send_player_turn_message(session=session)
    await send_to_player_turn_message(current_player=session.players[session.current_player])


async def prepare_char_message(session: Session, value: int):
    current_player = session.players[session.current_player]
    current_player.chars_message += f"{current_player.characteristics[value]}\n\n"


async def check_free_characteristics(callback: CallbackQuery, callback_data: MessageCallbackFactory, session: Session):
    session.selected_chars.append(callback_data.value)
    await prepare_char_message(session=session, value=callback_data.value)
    session.remove_char_from_player(player=session.current_player, index_of_char=callback_data.value)
    await send_edit_keyboard_of_char(callback=callback, session=session, group_id=session.id)
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


async def find_kicked_player(session: Session, message: Message):
    players_to_voiced: dict[int, int] = session.players_to_voiced
    kicked_player: int = max(players_to_voiced, key=players_to_voiced.get)
    kicked_player_index: int = 0
    player_nickname: str = ''
    for player in session.players:
        if player.id == kicked_player:
            player_nickname = player.name
            break
        else:
            kicked_player_index += 1
    session.remove_player(key=kicked_player, index=kicked_player_index)
    session.voiced_players = []
    session.players_to_voiced = {}
    await send_kicked_message(player_name=player_nickname, chat_id=session.id, session_db_id=session.db_id)
    if is_finish(session=session):
        await send_finished_message(chat_id=session.id, players=session.players)
        await clear_session(message=message)
    else:
        await turn(session=session)
