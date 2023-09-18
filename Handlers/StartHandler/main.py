from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from Database.methods import add_message_to_db
from Handlers.PrepareHandler.Methods.methods import add_player
from Handlers.StartHandler.Methods.methods import create_session, clear_session
from aiogram.fsm.context import FSMContext
from Models.Session import Session
from States.main import get_session
from Utils.conditions import is_unregistered_player, is_player
from Utils.helpers import is_session, get_group_context
from config import bot

start_router = Router()


@start_router.message(Command('start'), F.chat.type == "private")
async def sign_up_the_user(message: Message, command: CommandObject) -> None:
    try:
        state: FSMContext = await get_group_context(int(command.args))
        session: Session = await get_session(state=state)
        if is_unregistered_player(user_id=message.from_user.id, all_players=session.players_dict):
            await message.answer('Вы присоединилсь к партии')
            await add_player(message=message, session=session)
        else:
            await message.answer('Но ведь вы уже в партии, не так ли!?')
    except TypeError:
        await message.answer('Вы не выбрали сессию? Или возможно что-то пошло не так')


@start_router.message(Command('shelter'), F.chat.type.in_({'supergroup', 'group'}))
async def start_game_handler(message: Message, state: FSMContext) -> None:
    await create_session(message=message, state=state)
    await bot.delete_message(message.chat.id, message.message_id)


@start_router.message(Command('end'), F.chat.type.in_({'supergroup', 'group'}))
async def end_game_handler(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        await add_message_to_db(chat_id=message.chat.id, message_id=message.message_id, session_id=session.db_id)
        await clear_session(message=message)


@start_router.message()
async def block_unregister_players(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        user: int = message.from_user.id
        if not is_player(session=session, voiced_player_id=user):
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
