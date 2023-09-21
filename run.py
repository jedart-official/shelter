import asyncio

from aiogram import Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats

from Data.commands import set_group_commands
from Handlers.ProcessHandler.main import game_router
from Handlers.StartHandler.main import start_router
from config import bot, storage


async def main() -> None:
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT)
    dp.include_routers(start_router, game_router)
    await bot.set_my_commands(await set_group_commands(), BotCommandScopeAllGroupChats())
    await bot.set_my_commands((), BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
