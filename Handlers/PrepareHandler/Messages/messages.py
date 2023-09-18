from aiogram.types import BufferedInputFile, Message
from aiogram.utils.markdown import link
from Data.info import gifs
from Database.methods import add_message_to_db
from Models.Player import Player
from Keyboards.keyboards import set_markup, characteristics_of_player
from Models.Session import Session
from Models.Shelter import Shelter
from Utils.helpers import get_random_item_from_array
from config import bot


async def send_prepare_message(
    session: Session,
    all_players: dict[int, Player],
    max_players: int
) -> None:
    message_info = ''
    for player in all_players.values():
        player_link = link(player.name, f"https://t.me/{player.nickname}")
        message_info += f"|\t{player_link}\n"
    message_answer = await bot.edit_message_text(
        message_id=session.prepare_message_id,
        chat_id=session.id,
        text=f"Подготовка к игре: \n"
             f"{message_info}",
        reply_markup=set_markup(number=len(all_players), max_number=max_players, group_id=session.id),
        parse_mode='markdown',
        disable_web_page_preview=True
    )
    await add_message_to_db(message_answer.chat.id, message_answer.message_id, session.db_id)


async def send_start_game_message(player: Player, group_id: int) -> int:
    keyboard_chat: Message = await bot.send_message(
        chat_id=player.id,
        text=player.send_info_about_player(),
        parse_mode="MARKDOWN",
        reply_markup=characteristics_of_player(player.characteristic_names,
                                               group_id)
    )
    return keyboard_chat.message_id


async def delete_prepare_message(chat_id: int, message_id: int):
    await bot.delete_message(chat_id=chat_id, message_id=message_id)


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
        await add_message_to_db(message_id.chat.id, message_id.message_id, session_db_id)
