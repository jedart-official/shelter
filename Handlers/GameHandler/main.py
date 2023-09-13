from aiogram import Router, types
from Factories.MessageCallbackFactory import MessageCallbackFactory
from Factories.VoiceCallbackFactory import VoiceCallbackFactory
from Handlers.GameHandler.Conditions.conditions import is_current_player
from Handlers.GameHandler.Messages.messages import send_line_is_taken
from Handlers.GameHandler.Methods.methods import check_free_characteristics, find_kicked_player
from States.main import get_session
from Utils.helpers import get_group_context
from aiogram.fsm.context import FSMContext

game_router = Router()


@game_router.callback_query(MessageCallbackFactory.filter())
async def send_message(callback: types.CallbackQuery, callback_data: MessageCallbackFactory) -> None:
    state: FSMContext = await get_group_context(callback_data.group_id)
    if await is_current_player(callback=callback, state=state):
        await send_line_is_taken(callback=callback)
    else:
        await check_free_characteristics(callback=callback, callback_data=callback_data)


@game_router.callback_query(VoiceCallbackFactory.filter())
async def give_voice(callback: types.CallbackQuery, callback_data: VoiceCallbackFactory, state: FSMContext) -> None:
    session = await get_session(state=state)
    voiced_user: int = callback.from_user.id
    if voiced_user not in session.voiced_players:
        if not session.add_voiced_players(player_id=voiced_user, from_player=callback_data.value):
            await find_kicked_player(message=callback.message, state=state)
            return
