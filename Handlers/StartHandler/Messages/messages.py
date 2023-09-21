from aiogram import types
from aiogram.utils.markdown import link

from Data.static_messages import session_already_started_msg, select_count_players_msg, solo_playing_msg, \
    session_is_ended
from Database.methods import add_message_to_db
from Keyboards.keyboards import players_count, set_markup
from Models import Session
from Models.Player import Player
from config import bot


async def send_session_is_taken_message(message: types.Message, session_db_id: int) -> None:
    message_answer = await message.answer(
        text=session_already_started_msg,
        parse_mode="MARKDOWN"
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_id=session_db_id)


async def send_select_players_message(message: types.Message, session: Session) -> None:
    message_id = await message.answer(
        text=select_count_players_msg,
        reply_markup=players_count(),
        parse_mode="MARKDOWN"
    )
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


async def delete_prepare_message(chat_id: int, message_id: int):
    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


async def send_time_to_start_game_message(chat_id: int, time: int):
    await bot.send_message(chat_id=chat_id, text=f"Игра начнется через {time} секунд")


async def send_is_not_enough_players_message(chat_id: int):
    await bot.send_message(chat_id=chat_id, text=f"Игроков оказалось недостаточно. Сессия будет закрыта.")


async def send_edit_prepare_message(
        session: Session,
        all_players: dict[int, Player],
        max_players: int
) -> None:
    """
    Send a message about preparing to game | Show joined user
    :param session:
    :param all_players:
    :param max_players:
    """
    message_info = '\n |\t'.join([link(player.name, f"https://t.me/{player.nickname}") for player in all_players.values()])
    await bot.edit_message_text(
        message_id=session.prepare_message_id,
        chat_id=session.id,
        text=f"Присоединилсь к игре: \n"
             f"|{message_info}",
        reply_markup=set_markup(group_id=session.id),
        parse_mode='markdown',
        disable_web_page_preview=True
    )


async def send_prepare_message(
        session: Session,
        all_players: dict[int, Player],
        max_players: int
) -> None:
    """
    Send a message about preparing to game | Show joined user
    :param session:
    :param all_players:
    :param max_players:
    """
    message_info = '\n'.join(
        [link(player.name, f"https://t.me/{player.nickname}") for player in all_players.values()])
    message_answer = await bot.send_message(
        chat_id=session.id,
        text=f"Подготовка к игре: \n"
             f"{message_info}",
        reply_markup=set_markup(group_id=session.id),
        parse_mode='markdown',
        disable_web_page_preview=True
    )
    session.prepare_message_id = message_answer.message_id
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)
