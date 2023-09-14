from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from Handlers.GameHandler.Conditions.conditions import is_player
from Handlers.ProcessHandler.Methods.methods import create_session, clear_session
from aiogram.fsm.context import FSMContext
from Models.Session import Session
from States.main import get_session
from Utils.helpers import is_session
from config import bot

process_router = Router()


@process_router.message(Command('start'))
async def sign_up_the_user(message: Message) -> None:
    await message.answer('Регистрация прошла успешно')


@process_router.message(Command('shelter'))
async def start_game_handler(message: Message, state: FSMContext) -> None:
    await create_session(message=message, state=state)


@process_router.message(Command('end'))
async def end_game_handler(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        await clear_session(message=message)


@process_router.message()
async def block_unregister_players(message: Message, state: FSMContext) -> None:
    if await is_session(state=state):
        session: Session = await get_session(state=state)
        user: int = message.from_user.id
        if not is_player(session=session, voiced_player_id=user):
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
