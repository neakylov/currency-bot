import requests

from aiogram import types
from loader import dp
from aiogram.filters.command import Command
from aiogram.filters import Text
from data import config
from keyboards.default.start_buttons import start_buttons
from keyboards.inline.pagination import pagination


def get_data():
    response = requests.get(config.URL).json()
    currencies = response.get('conversion_rates')
    text = []
    for curr in currencies:
        text.append(f'\n{curr}: {currencies[curr]}')
    return text


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hello! '
                         f'This bot sends the exchange rate against the dollar.'
                         f'\nClick the "Exchange rate" button.',
                         reply_markup=start_buttons())


@dp.message(Text('Exchange rate'))
async def exchange(message: types.Message):
    text = get_data()
    await message.reply(''.join(text[:25]), reply_markup=pagination(page=1))


@dp.callback_query(Text(startswith='page_'))
async def callbacks_page(callback: types.CallbackQuery):
    data = callback.data.split('_')
    action = data[1]
    page = int(data[2])
    if action == 'next':
        text = get_data()
        new_page = page + 1
        second_item = 25 * new_page
        first_item = second_item - 25
        await callback.message.edit_text(''.join(text[first_item:second_item]), reply_markup=pagination(page=new_page))
    elif action == 'back':
        text = get_data()
        new_page = page - 1
        second_item = 25 * new_page
        first_item = second_item - 25
        await callback.message.edit_text(''.join(text[first_item:second_item]), reply_markup=pagination(page=new_page))
    elif action == 'middle':
        await callback.answer(f'Page:{page}',)
    else:
        await callback.message.answer('Error! Send "/start".')