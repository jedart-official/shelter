from aiogram.types import CallbackQuery, BufferedInputFile, Message
from aiogram.utils.markdown import link

from Data.info import gifs
from Data.static_messages import *
from Database.methods import add_message_to_db
from Keyboards.keyboards import edited_characteristics_of_player, \
    players_nickname, characteristics_of_player
from Models.Player import Player
from Models.Session import Session
from Models.Shelter import Shelter
from Utils.helpers import get_random_item_from_array
from config import bot


async def send_line_is_taken(callback: CallbackQuery) -> None:
    await callback.answer(
        text=is_not_turn_msg,
        show_alert=True,
    )


async def send_information_message(session: Session) -> None:
    player_key = session.current_player
    player: Player = session.players_dict[player_key]
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


async def send_edit_keyboard_of_char(message_id: int, session: Session, group_id: int) -> None:
    current_player = session.players_dict[session.current_player]
    current_player_chars: list = current_player.characteristic_names
    await bot.edit_message_reply_markup(
        chat_id=session.id,
        message_id=message_id,
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


async def send_to_player_turn_message(chars_count: int, current_player: Player):
    await bot.send_message(
        chat_id=current_player.id,
        text=f'{current_player.name},  вам необходимо выбрать {chars_count} характеристики',
        parse_mode='markdown',
    )


async def send_player_turn_message(session: Session) -> None:
    current_player: Player = session.players_dict[session.current_player]
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
    voiced_players = [session.players_dict[player] for player in session.voiced_players]
    message = '\n'.join([f'_{player.job}_\t|\t *{player.name}*' for player in voiced_players]).upper()
    text = f'{start_voice_msg}:\n\nПроголосовавшие:\n{message}'
    message_answer = await bot.edit_message_text(
        text=text,
        chat_id=session.id,
        message_id=message_id,
        reply_markup=players_nickname(list(session.players_dict.values())),
        parse_mode="markdown"
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)


async def send_start_meeting_message(session: Session) -> None:
    await send_empty_message(chat_id=session.id, session_db_id=session.db_id)
    message_answer = await bot.send_message(
        text=start_voice_msg,
        chat_id=session.id,
        reply_markup=players_nickname(list(session.players_dict.values())),
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







async def send_start_game_message(player: Player, group_id: int) -> int:
    keyboard_chat: Message = await bot.send_message(
        chat_id=player.id,
        text=player.send_info_about_player(),
        parse_mode="MARKDOWN",
        reply_markup=characteristics_of_player(
            player.characteristic_names,
            group_id
        )
    )
    return keyboard_chat.message_id


async def send_history_message(chat_id: int, shelter: Shelter, session_db_id: int) -> None:
    random_path = get_random_item_from_array(array=gifs)
    with open(random_path, 'rb') as image_gif:
        message_id = await bot.send_animation(
            animation=BufferedInputFile(
                image_gif.read(),
                filename="base_photo.gif"
            ),
            width=500,
            chat_id=chat_id,
            caption=f"<b>ПРЕДИСТОРИЯ:</b> \n"
                    f"{shelter.history['description']} \n\n"
                    f"<b>ПРИМЕЧАНИЕ:</b> \n"
                    f"{shelter.history['notice']} \n\n"
                    f"<b>БУНКЕР</b>:\n"
                    f"<i>ТИП БУНКЕРА</i> | <b>{shelter.shelter_info['type']}</b> \n"
                    f"<i>ЛОКАЦИЯ</i> | <b>{shelter.shelter_info['location']}</b> \n"
                    f"<i>СОСТОЯНИЕ БУНКЕРА</i> | <b>{shelter.shelter_info['state']}</b> \n"
                    f"<i>ГЛАВНАЯ КОМНАТА</i> | <b>{shelter.shelter_info['main_room']}</b> \n"
                    f"<i>ДОП.КОМНАТА</i> | <b>{shelter.shelter_info['additional_room']}</b> \n"
                    f"<i>СОДЕРЖИМОЕ БУНКЕРА</i> | <b>{shelter.shelter_info['invertory']}</b> \n\n"
                    f"<b>УСЛОВИЯ ВЫЖИВАНИЯ</b>:\n"
                    f"<i>КОЛИЧЕСТВО ЧЕЛОВЕК</i> | <b>{shelter.players_in_shelter}</b> \n"
                    f"<i>ВРЕМЯ ВЫЖИВАНИЯ</i> | <b>{shelter.live_time}</b>",
            parse_mode='HTML'
        )
        shelter.clear_some_info_about_shelter()
        await bot.pin_chat_message(message_id.chat.id, message_id.message_id)
        await add_message_to_db(message_id.chat.id, message_id.message_id, session_db_id)
