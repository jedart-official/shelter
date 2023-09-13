from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputFile, BufferedInputFile
from Data.static_messages import prepare_to_game_msg
from Models.Player import Player
from Keyboards.keyboards import set_markup, characteristics_of_player
from Models.Session import Session
from Models.Shelter import Shelter
from States.main import get_session
from config import bot


async def send_prepare_message(callback: CallbackQuery,
                               all_players: dict[int, Player], max_players: int) -> None:
    await bot.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        text=prepare_to_game_msg,
        reply_markup=set_markup(number=len(all_players), max_number=max_players)
    )


async def send_start_game_message(player: Player, group_id: int) -> None:
    await bot.send_message(chat_id=player.id, text=player.send_info_about_player(), parse_mode="MARKDOWN",
                           reply_markup=characteristics_of_player(player.characteristic_names, group_id))


async def send_history_message(callback: CallbackQuery, state: FSMContext) -> None:
    session: Session = await get_session(state=state)
    shelter: Shelter = session.shelter
    with open("Data/base_photo.gif", 'rb') as image_gif:
        await bot.send_photo(
            photo=BufferedInputFile(
                image_gif.read(),
                filename="image from buffer.jpg"
            ),
            chat_id=callback.message.chat.id,
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
