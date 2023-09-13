from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from Data.static_messages import *
from Factories.MessageCallbackFactory import MessageCallbackFactory
from States.main import get_session
from Models.Player import Player
from Keyboards.keyboards import edited_characteristics_of_player, \
    players_nickname
from Models.Session import Session
from config import bot


async def send_line_is_taken(callback: CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text=is_not_turn_msg,
                           parse_mode='MARKDOWN')


async def send_characteristics_is_full_message(callback: CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text=enough_chars,
                           parse_mode='MARKDOWN')


async def send_information_message(callback_data: MessageCallbackFactory, state: FSMContext) -> None:
    context = await state.get_data()
    session: Session = context['session']
    player_index = session.current_player
    player: Player = session.players[player_index]
    await bot.send_message(chat_id=session.id,
                           text=f"*ИНФОРМАЦИЯ ОБ* |  {player.name.upper()}\n{player.characteristics[callback_data.value]}",
                           parse_mode='MARKDOWN')


async def send_edit_keyboard_of_char(callback: CallbackQuery, player: Player, group_id: int) -> None:
    current_player_chars: list = player.characteristic_names
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=edited_characteristics_of_player(
                                            current_player_chars, group_id=group_id))


async def send_empty_message(state: FSMContext):
    session: Session = await get_session(state=state)
    await bot.send_message(
        chat_id=session.id,
        text=f"{empty_msg}\n\n",
    )


async def send_turn_message(state: FSMContext) -> None:
    session_data: dict[any, any] = await state.get_data()
    session: Session = session_data['session']
    await bot.send_message(
        chat_id=session.id,
        text=f'\n\n❗️ Начинается {session.current_turn} круг игры.❗'
             f'\nКаждый из вас раскрывает {session.important_open} свои характеристики '.upper(),
    )


async def send_player_turn_message(state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    current_player: Player = session.players[session.current_player]
    await bot.send_message(
        chat_id=session.id,
        text=f'{empty_msg}\n\n {current_player.name}, раскройте {session.important_open} свои характеристики \n\n {empty_msg}'.upper(),
    )


async def send_start_meeting_message(state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    await send_empty_message(state=state)
    await bot.send_message(text=start_voice_msg,
                           chat_id=session.id,
                           reply_markup=players_nickname(session.players))


async def send_kicked_message(player_name: str, state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    await bot.send_message(text=f"{voiced_to_msg} {player_name} ", chat_id=session.id)


async def send_finished_message(state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    message: str = ''
    for player in session.players:
        message += f'\n {player.name}'

    await bot.send_message(text=f"{congr_with_win_msg} {message} ", chat_id=session.id)
