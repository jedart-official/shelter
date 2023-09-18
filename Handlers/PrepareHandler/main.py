from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from States.main import get_session
from Factories.NumberCallbackFactory import NumbersCallbackFactory
from Handlers.PrepareHandler.Messages.messages import send_prepare_message
from Models.Session import Session
from Models.Shelter import Shelter
from Utils.helpers import is_session

prepare_router = Router()


@prepare_router.callback_query(NumbersCallbackFactory.filter(), F.chat.type.in_({'group', 'supergroup'}))
async def set_number_of_players_in_game(callback: types.CallbackQuery,  callback_data: NumbersCallbackFactory,
                                        state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        max_players: int = callback_data.value
        shelter: Shelter = Shelter(max_players=max_players)
        session.max_players = max_players
        session.shelter = shelter
        await send_prepare_message(session=session, all_players=session.players_dict,
                                   max_players=session.max_players)
