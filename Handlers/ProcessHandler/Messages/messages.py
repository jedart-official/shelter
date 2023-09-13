from aiogram import types
from Data.static_messages import session_already_started_msg, select_count_players_msg, solo_playing_msg, \
    session_is_ended
from Keyboards.keyboards import players_count


async def send_session_is_taken_message(message: types.Message) -> None:
    await message.answer(text=session_already_started_msg,
                         parse_mode="MARKDOWN")


async def send_select_players_message(message: types.Message) -> None:
    await message.answer(text=select_count_players_msg, reply_markup=players_count(),
                         parse_mode="MARKDOWN")


async def send_solo_playing_message(message: types.Message) -> None:
    await message.answer(
        solo_playing_msg,
        parse_mode="MARKDOWN")


async def send_end_game_message(message: types.Message) -> None:
    await message.answer(text=session_is_ended,
                         parse_mode="MARKDOWN")
