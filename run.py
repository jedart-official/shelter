import asyncio
import logging
import sys
from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats

from Data.commands import set_group_commands, set_private_commands
from Handlers.GameHandler.main import game_router
from States.main import memory_router
from Handlers.PrepareHandler.main import prepare_router
from Handlers.ProcessHandler.main import process_router
from config import bot, storage
from aiogram.fsm.strategy import FSMStrategy


async def main() -> None:
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT)
    dp.include_routers(process_router, prepare_router, game_router, memory_router)
    await bot.set_my_commands(await set_group_commands(), BotCommandScopeAllGroupChats())
    await bot.set_my_commands(await set_private_commands(), BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
