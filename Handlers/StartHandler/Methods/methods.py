from aiogram.types import Message
from Database.main import session_db, SessionDB
from States.main import update_session, get_session
from Models.Session import Session
from Handlers.StartHandler.Messages.messages import send_session_is_taken_message, send_select_players_message, \
    send_end_game_message
from aiogram.fsm.context import FSMContext
from Utils.helpers import is_session, get_group_context, clear_group_messages


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
        await send_select_players_message(message=message, session=new_session)


async def clear_session(message: Message) -> None:
    state: FSMContext = await get_group_context(message.chat.id)
    session: Session = await get_session(state=state)
    await clear_group_messages(chat_id=message.chat.id, session_id=session.db_id)
    await state.clear()
    await send_end_game_message(message=message)
