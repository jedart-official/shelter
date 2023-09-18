from aiogram import types
from Data.static_messages import session_already_started_msg, select_count_players_msg, solo_playing_msg, \
    session_is_ended
from Database.methods import add_message_to_db
from Keyboards.keyboards import players_count
from Models import Session


async def send_session_is_taken_message(message: types.Message, session_db_id: int) -> None:
    message_answer = await message.answer(text=session_already_started_msg,
                                          parse_mode="MARKDOWN")
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_id=session_db_id)


async def send_select_players_message(message: types.Message, session: Session) -> None:
    message_id = await message.answer(text=select_count_players_msg, reply_markup=players_count(),
                                      parse_mode="MARKDOWN")
    session.prepare_message_id = message_id.message_id


async def send_solo_playing_message(message: types.Message) -> None:
    await message.answer(
        solo_playing_msg,
        parse_mode="MARKDOWN")


async def send_end_game_message(message: types.Message) -> None:
    await message.answer(
        text=session_is_ended,
        parse_mode="MARKDOWN"
    )
