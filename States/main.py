from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from Models.Session import Session


class ActiveSession(StatesGroup):
    session: Session = State()


async def update_session(session: Session, state: FSMContext):
    await state.update_data(session=session)


async def get_session(state: FSMContext) -> Session:
    session_data = await state.get_data()
    return session_data['session']
