from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from States.main import get_session, update_session
from Factories.NumberCallbackFactory import NumbersCallbackFactory
from Models.Player import Player
from Handlers.PrepareHandler.Conditions.conditions import is_unreg_player, is_full_party
from Handlers.PrepareHandler.Messages.messages import send_prepare_message
from Handlers.PrepareHandler.Methods.methods import create_player, prepare_game, run_game_message
from Models.Session import Session
from Models.Shelter import Shelter

prepare_router = Router()


@prepare_router.callback_query(NumbersCallbackFactory.filter())
async def set_number_of_players_in_game(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory,
                                        state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    max_players: int = callback_data.value
    shelter: Shelter = Shelter(max_players=max_players)
    session.max_players = max_players
    session.shelter = shelter
    await add_player(callback=callback, state=state)


@prepare_router.callback_query(F.data == 'add_player')
async def add_player(callback: types.CallbackQuery, state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    print(callback.from_user.id)
    if is_unreg_player(callback=callback, all_players=session.players_dict):
        all_players: dict[int, Player] = session.players_dict
        all_players[callback.from_user.id] = create_player(callback=callback)
        await send_prepare_message(callback=callback, all_players=all_players, max_players=session.max_players)
        if is_full_party(all_players=all_players, players_in_game=session.max_players):
            await prepare_game(state=state)
            await run_game_message(callback=callback, state=state)
