import logging

from data.config import ADMINS
from aiogram import Bot


async def on_startup(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, 'Bot was started!')
        except Exception as exc:
            logging.exception(exc)


async def on_shutdown(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, 'Bot was stopped!')
        except Exception as exc:
            logging.exception(exc)