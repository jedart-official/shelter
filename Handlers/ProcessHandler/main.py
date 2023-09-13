from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from Handlers.GameHandler.Conditions.conditions import is_session
from Handlers.ProcessHandler.Methods.methods import create_session, clear_session
from aiogram.fsm.context import FSMContext

process_router = Router()


@process_router.message(Command('start'))
async def sign_up_the_user(message: Message) -> None:
    await message.answer('Регистрация прошла успешно')


@process_router.message(Command('shelter'))
async def start_game_handler(message: Message, state: FSMContext) -> None:
    await create_session(message=message, state=state)


@process_router.message(Command('end'))
async def end_game_handler(message: Message, state: FSMContext) -> None:
    if is_session(state=state):
        await clear_session(message=message, state=state)
