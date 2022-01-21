import os
from dotenv import load_dotenv

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


cfg = load_dotenv(".env")


bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
