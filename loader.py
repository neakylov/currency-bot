from aiogram import Bot, Dispatcher
from aiogram.enums import parse_mode
from aiogram.fsm.storage.memory import MemoryStorage
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=parse_mode.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)