from aiogram.types import Message
from States.main import update_session
from Models.Session import Session
from Handlers.ProcessHandler.Messages.messages import send_session_is_taken_message, send_select_players_message, \
    send_end_game_message
from aiogram.fsm.context import FSMContext

from Utils.helpers import get_group_context, is_session


async def create_session(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        await send_session_is_taken_message(message=message)
    else:
        new_session: Session = Session(session_id=message.chat.id)
        await update_session(state=state, session=new_session)
        await send_select_players_message(message=message)


async def clear_session(message: Message) -> None:
    state: FSMContext = await get_group_context(message.chat.id)
    await state.clear()
    await send_end_game_message(message=message)
