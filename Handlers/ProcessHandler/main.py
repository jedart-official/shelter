from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from Factories.MessageCallbackFactory import MessageCallbackFactory
from Factories.VoiceCallbackFactory import VoiceCallbackFactory
from Handlers.ProcessHandler.Messages.messages import send_edit_meeting_message
from Handlers.ProcessHandler.Methods.methods import check_free_characteristics, send_kicked_player
from Models.Session import Session
from States.main import get_session
from Utils.conditions import is_current_player, is_current_user_keyboard, is_player
from Utils.helpers import get_group_context, is_session

game_router = Router()


@game_router.callback_query(MessageCallbackFactory.filter())
async def send_message(callback: types.CallbackQuery, callback_data: MessageCallbackFactory) -> None:
    state: FSMContext = await get_group_context(callback_data.group_id)
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        if is_current_player(callback=callback, session=session) and is_current_user_keyboard(
                message_id=callback.message.message_id,
                keywords=session.keyboards
        ):
            await check_free_characteristics(callback=callback, callback_data=callback_data, session=session)


@game_router.callback_query(VoiceCallbackFactory.filter())
async def give_voice(callback: types.CallbackQuery, callback_data: VoiceCallbackFactory, state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        voiced_user: int = callback.from_user.id
        if is_player(session=session, voiced_player_id=voiced_user):
            if voiced_user not in session.voiced_players:
                if not session.add_voiced_players(player_id=voiced_user, from_player=callback_data.value):
                    await send_kicked_player(message=callback.message, session=session)
                    return
                else:
                    await send_edit_meeting_message(session=session, message_id=callback.message.message_id)
