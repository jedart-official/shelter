from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from Models.Session import Session
from Utils.helpers import get_group_context, clear_group_messages


class ActiveSession(StatesGroup):
    session: Session = State()


async def update_session(session: Session, state: FSMContext):
    await state.update_data(session=session)


async def get_session(state: FSMContext) -> Session:
    session_data = await state.get_data()
    return session_data['session']


async def clear_session(message: Message) -> None:
    state: FSMContext = await get_group_context(message.chat.id)
    session = await get_session(state=state)
    await clear_group_messages(chat_id=message.chat.id, session_id=session.db_id)
    await state.clear()
