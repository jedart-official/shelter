from os import getenv

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = getenv('TOKEN')
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
