import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Database.main import session_db, SessionDB
from Handlers.ProcessHandler.Methods.methods import start_game_manager
from Handlers.StartHandler.Messages.messages import send_session_is_taken_message, send_time_to_start_game_message, \
    delete_prepare_message, send_is_not_enough_players_message, send_end_game_message, send_edit_prepare_message, \
    send_prepare_message
from Models.Player import create_player, Player
from Models.Session import Session
from States.main import update_session, get_session, clear_session
from Utils.helpers import is_session


async def create_session(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        await send_session_is_taken_message(message=message, session_db_id=session.db_id)
    else:
        db_session: SessionDB = SessionDB()
        session_db.add(db_session)
        session_db.commit()
        new_session: Session = Session(session_id=message.chat.id, db_id=db_session.id)
        await update_session(state=state, session=new_session)
        session: Session = await get_session(state=state)
        await send_prepare_message(
            session=session,
            all_players=new_session.players_dict,
            max_players=new_session.max_players
        )
        await set_timer_for_start_game(message=message, session=session, delay_seconds=60)


async def add_player(message: Message, session: Session) -> None:
    all_players: dict[int, Player] = session.players_dict
    new_player_id: int = message.from_user.id
    if len(all_players) == 0:
        session.current_player = new_player_id
    all_players[new_player_id] = create_player(message=message)
    await send_edit_prepare_message(
        session=session,
        all_players=session.players_dict,
        max_players=session.max_players
    )


async def set_timer_for_start_game(delay_seconds: int, session: Session, message: Message):
    await send_time_to_start_game_message(chat_id=session.id, time=delay_seconds)
    await asyncio.sleep(delay_seconds)
    if len(session.players_dict) >= 4:
        await delete_prepare_message(chat_id=session.id, message_id=session.prepare_message_id)
        await start_game_manager(session=session)
    else:
        await send_is_not_enough_players_message(chat_id=session.id)
        await clear_session(message=message)
        await send_end_game_message(message=message)
