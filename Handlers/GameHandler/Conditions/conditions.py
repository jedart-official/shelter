from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from States.main import get_session
from Models import Player
from Models.Session import Session
from Models.Shelter import Shelter


async def is_session(state: FSMContext) -> bool:
    session_data = await state.get_data()
    return 'session' in session_data


async def is_current_player(callback: CallbackQuery, state: FSMContext) -> bool:
    from_user = callback.from_user.id
    session: Session = await get_session(state=state)
    current_session_player: Player = session.players[session.current_player]
    current_session_player_id: int = current_session_player.id
    return from_user != current_session_player_id


async def is_finish(state: FSMContext) -> bool:
    session: Session = await get_session(state=state)
    shelter: Shelter = session.shelter
    return len(session.players) == shelter.players_in_shelter


async def is_free_characteristic(state: FSMContext) -> bool | str:
    session: Session = await get_session(state=state)
    opened: int = session.opened_characteristic
    important: int = session.important_open
    return opened <= important


async def is_voice_turn(state: FSMContext) -> bool:
    session: Session = await get_session(state=state)
    shelter: Shelter = session.shelter
    return session.current_turn >= shelter.voice_turn
