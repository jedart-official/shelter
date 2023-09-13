from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from Factories.MessageCallbackFactory import MessageCallbackFactory
from States.main import get_session
from Handlers.ProcessHandler.Methods.methods import clear_session
from Models.Player import Player
from Handlers.GameHandler.Conditions.conditions import is_free_characteristic, is_finish, is_voice_turn, is_session
from Handlers.GameHandler.Messages.messages import send_characteristics_is_full_message, send_information_message, \
    send_edit_keyboard_of_char, send_turn_message, send_player_turn_message, send_start_meeting_message, \
    send_kicked_message, send_finished_message
from Models.Session import Session
from Utils.helpers import get_group_context


async def turn(state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        session.opened_characteristic = 0
        session.current_player = 0
        session.current_turn += 1
        await send_turn_message(state=state)
        await player_turn_message(state=state)


async def player_turn_message(state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        session.opened_characteristic = 0
        await send_player_turn_message(state=state)


async def check_free_characteristics(callback: CallbackQuery, callback_data: MessageCallbackFactory):
    group_id: int = callback_data.group_id
    state: FSMContext = await get_group_context(chat_id=group_id)
    session: Session = await get_session(state=state)
    session.inc_opened_characteristic()
    if await is_free_characteristic(state=state):
        await turn_of_player(callback=callback, callback_data=callback_data)
    await is_incremented_player(state=state)


async def is_incremented_player(state: FSMContext):
    session: Session = await get_session(state=state)
    if session.opened_characteristic == session.important_open:
        if session.inc_current_player():
            await player_turn_message(state=state)
        else:
            await voice_turn(state=state)


async def voice_turn(state: FSMContext):
    if await is_voice_turn(state=state):
        await send_start_meeting_message(state=state)
    else:
        await turn(state=state)


async def turn_of_player(callback: CallbackQuery, callback_data: MessageCallbackFactory) -> None:
    group_id: int = callback_data.group_id
    state: FSMContext = await get_group_context(group_id)
    session: Session = await get_session(state=state)
    player_index: int = session.current_player
    player: Player = session.players[player_index]
    await send_information_message(callback_data=callback_data, state=state)
    session.remove_char_from_player(player=player_index, index_of_char=callback_data.value)

    await send_edit_keyboard_of_char(callback=callback, player=player, group_id=group_id)


async def find_kicked_player(state: FSMContext, message: Message):
    session: Session = await get_session(state=state)
    players_to_voiced: dict[int, int] = session.players_to_voiced
    kicked_player: int = max(players_to_voiced, key=players_to_voiced.get)
    kicked_player_index: int = 0
    player_nickname: str = ''
    for player in session.players:
        if player.id == kicked_player:
            player_nickname = player.name
            break
        else:
            kicked_player_index += 1
    session.remove_player(key=kicked_player, index=kicked_player_index)
    session.voiced_players = []
    session.players_to_voiced = {}
    await send_kicked_message(player_nickname, state=state)
    if await is_finish(state=state):
        await send_finished_message(state=state)
        await clear_session(message=message, state=state)
    else:
        await turn(state=state)
