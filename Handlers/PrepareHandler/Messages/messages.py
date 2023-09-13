from aiogram.types import CallbackQuery
from Data.static_messages import prepare_to_game_msg, start_game_msg
from Models.Player import Player
from Keyboards.keyboards import set_markup, characteristics_of_player
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


async def send_run_game_message(callback: CallbackQuery) -> None:
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=start_game_msg,
    )
