from aiogram import types
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
from aiogram.utils.markdown import link, hlink


async def send_line_is_taken(callback: CallbackQuery) -> None:
    await callback.answer(
        text=is_not_turn_msg,
        show_alert=True,
    )


async def send_characteristics_is_full_message(callback: CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text=enough_chars,
                           parse_mode='MARKDOWN')


async def send_information_message(callback_data: MessageCallbackFactory, state: FSMContext) -> None:
    context = await state.get_data()
    session: Session = context['session']
    player_index = session.current_player
    player: Player = session.players[player_index]
    str_link = f'https://t.me/{player.nickname}'
    player_name_link = link(player.name.upper(), str_link)
    await bot.send_message(
        chat_id=session.id,
        text=f"*ИНФОРМАЦИЯ ОБ* |  {player_name_link} | *{player.job}* \n{player.characteristics[callback_data.value]}".upper(),
        parse_mode='MARKDOWN',
        disable_web_page_preview=True
    )


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
        text=f'❗\t Начинается {session.current_turn} круг игры. \t ❗'.upper(),
    )


async def send_player_turn_message(state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    current_player: Player = session.players[session.current_player]
    str_link = f'https://t.me/{current_player.nickname}'
    player_name_link = link(current_player.name, str_link)
    await bot.send_message(
        chat_id=session.id,
        text=f'{empty_msg}\n'
             f'_Показывает характеристики_ \t|\t  {player_name_link} \n'
             f'_Количество_ \t|\t *{session.important_open}* \n '
             f'{empty_msg}'.upper(),
        parse_mode='markdown',
        disable_web_page_preview=1
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
        str_link = f'https://t.me/{player.nickname}'
        player_name_link = link(player.name, str_link)
        message += f'*{player.job.upper()}* \t|\t {player_name_link} \n'

    await bot.send_message(
        text=f"*Игра завершена!* \n\n{congr_with_win_msg}\n{message} ",
        chat_id=session.id,
        parse_mode='MARKDOWN',
        disable_web_page_preview=True)
