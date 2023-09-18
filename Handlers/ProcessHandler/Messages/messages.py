from aiogram.types import CallbackQuery, BufferedInputFile
from Data.static_messages import *
from Database.methods import add_message_to_db
from Models.Player import Player
from Keyboards.keyboards import edited_characteristics_of_player, \
    players_nickname
from Models.Session import Session
from config import bot
from aiogram.utils.markdown import link


async def send_line_is_taken(callback: CallbackQuery) -> None:
    await callback.answer(
        text=is_not_turn_msg,
        show_alert=True,
    )


async def send_information_message(session: Session) -> None:
    player_index = session.current_player
    player: Player = session.players[player_index]
    str_link = f'https://t.me/{player.nickname}'
    player_name_link = link(player.name.upper(), str_link)
    message_answer = await bot.send_message(
        chat_id=session.id,
        text=f"*ИНФОРМАЦИЯ ОБ* |  {player_name_link} | *{player.job}* \n\n"
             f"{player.chars_message}",
        parse_mode='MARKDOWN',
        disable_web_page_preview=True
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_id=session.db_id)


async def send_edit_keyboard_of_char(callback: CallbackQuery, session: Session, group_id: int) -> None:
    current_player = session.players[session.current_player]
    current_player_chars: list = current_player.characteristic_names
    await bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=edited_characteristics_of_player(
            current_player_chars, group_id=group_id)
    )


async def send_empty_message(chat_id: int, session_db_id: int):
    message_answer = await bot.send_message(
        chat_id=chat_id,
        text=f"{empty_msg}\n\n",
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_db_id)


async def send_turn_message(chat_id: int, current_turn: int, session_db_id: int) -> None:
    message_answer = await bot.send_message(
        chat_id=chat_id,
        text=f'❗\t Начинается {current_turn} круг игры. \t ❗'.upper(),
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_db_id)


async def send_to_player_turn_message(current_player: Player):
    await bot.send_message(
        chat_id=current_player.id,
        text=f'{current_player.name}, время раскрыть характеристики',
        parse_mode='markdown',
    )


async def send_player_turn_message(session: Session) -> None:
    current_player: Player = session.players[session.current_player]
    str_link = f'https://t.me/{current_player.nickname}'
    player_name_link = link(current_player.name, str_link)
    message_answer = await bot.send_message(
        chat_id=session.id,
        text=f'{empty_msg}\n'
             f'_Показывает характеристики_ \t|\t  {player_name_link} \n'
             f'_Количество_ \t|\t *{session.important_open}* \n '
             f'{empty_msg}'.upper(),
        parse_mode='markdown',
        disable_web_page_preview=1
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)


async def send_edit_meeting_message(session: Session, message_id: int) -> None:
    voiced_players: list[Player] = list()
    for player in session.voiced_players:
        voiced_players.append(session.players_dict[player])
    message: str = ''
    for player in voiced_players:
        message += f'_{player.job}_\t|\t *{player.name}*\n'.upper()
    message_answer = await bot.edit_message_text(
        text=f'{start_voice_msg}:\n\n'
             f'Проголосовавшие:\n'
             f'{message}',
        chat_id=session.id,
        message_id=message_id,
        reply_markup=players_nickname(session.players),
        parse_mode="markdown"
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)


async def send_start_meeting_message(session: Session) -> None:
    await send_empty_message(chat_id=session.id, session_db_id=session.db_id)
    message_answer = await bot.send_message(
        text=start_voice_msg,
        chat_id=session.id,
        reply_markup=players_nickname(session.players),
        parse_mode="markdown"
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)


async def send_kicked_message(player_name: str, chat_id: int, session_db_id: int) -> None:
    with open('Data/Images/bunker_dead.png', 'rb') as photo:
        message_answer = await bot.send_photo(
            photo=BufferedInputFile(
                photo.read(),
                filename='bunker_dead.png'
            ),
            caption=f"{voiced_to_msg} {player_name} ",
            chat_id=chat_id
        )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session_db_id)


async def send_finished_message(chat_id: int, players: list[Player]) -> None:
    message: str = ''
    for player in players:
        str_link = f'https://t.me/{player.nickname}'
        player_name_link = link(player.name, str_link)
        message += f'*{player.job.upper()}* \t|\t {player_name_link} \n'

    await bot.send_message(
        text=f"*Игра завершена!* \n\n{congr_with_win_msg}\n{message} ",
        chat_id=chat_id,
        parse_mode='MARKDOWN',
        disable_web_page_preview=True)
