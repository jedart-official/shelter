from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from Factories.MessageCallbackFactory import MessageCallbackFactory
from Factories.NumberCallbackFactory import NumbersCallbackFactory
from Factories.VoiceCallbackFactory import VoiceCallbackFactory
from Models.Player import Player


def set_markup(group_id: int) -> InlineKeyboardMarkup:
    start_btn = InlineKeyboardButton(
        text=f"Присоедениться к игре",
        callback_data='add_player',
        url=f'https://t.me/shelter_is_bot?start={group_id}'
    )
    start_markup = InlineKeyboardBuilder()
    start_markup.add(start_btn)
    return start_markup.as_markup()


def characteristics_of_player(array: list, group_id: int) -> InlineKeyboardMarkup:
    characteristics_of_player_markup = InlineKeyboardBuilder()
    for index in range(0, len(array)):
        characteristics_of_player_markup.button(
            text=f"{array[index]}",
            callback_data=MessageCallbackFactory(
                action='send_message',
                value=index,
                group_id=group_id
            )
        )
    characteristics_of_player_markup.adjust(1)
    return characteristics_of_player_markup.as_markup()


def edited_characteristics_of_player(player_chars: list, group_id) -> InlineKeyboardMarkup:
    return characteristics_of_player(player_chars, group_id=group_id)


def players_count() -> InlineKeyboardMarkup:
    max_players: int = 9
    players_count_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for player in range(1, max_players):
        players_count_markup.button(
            text=f"{player}",
            callback_data=NumbersCallbackFactory(action="set_players", value=player))
    players_count_markup.adjust(2)
    return players_count_markup.as_markup()


def players_nickname(players: list[Player]) -> InlineKeyboardMarkup:
    players_nicknames_markup: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for player in players:
        players_nicknames_markup.button(
            text=player.name,
            callback_data=VoiceCallbackFactory(action='give_voice', value=player.id))
    players_nicknames_markup.adjust(1)
    return players_nicknames_markup.as_markup()
