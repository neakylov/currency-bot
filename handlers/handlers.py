import requests

from aiogram import types
from loader import dp
from aiogram.filters.command import Command
from aiogram.filters import Text
from data import config


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    buttons = [
        [
            types.KeyboardButton(text='Exchange rate')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    await message.answer(f'Hello! '
                         f'This bot sends the exchange rate against the dollar.'
                         f'\nClick the "Exchange rate" button.',
                         reply_markup=keyboard)


@dp.message(Text('Exchange rate'))
async def exchange(message: types.Message):
    response = requests.get(config.URL).json()
    currencies = response.get('conversion_rates')
    text = []
    for curr in currencies:
        text.append(f'\n{curr}: {currencies[curr]}')
    await message.reply(''.join(text))