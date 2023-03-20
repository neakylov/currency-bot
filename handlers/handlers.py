import requests

from aiogram import types
from loader import dp
from aiogram.filters.command import Command
from aiogram.filters import Text
from data import config
from keyboards.default.start_buttons import start_buttons
from keyboards.inline.pagination import pagination
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Language(StatesGroup):
    lang = State()


class ExchangeRate(StatesGroup):
    text = State()


def get_data():
    response = requests.get(config.URL).json()
    currencies = response.get('conversion_rates')
    text = []
    for curr in currencies:
        text.append(f'\n{curr}: {currencies[curr]}')
    return text


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет! '
                         f'Этот бот знает курс валют к доллару.'
                         f'\n* Нажми кнопку "Курс валют" чтобы узнать нынешний курс.'
                         f'\n* Нажми кнопку "Конвертер валют" чтобы конвертировать валюту.',
                         reply_markup=start_buttons())


@dp.message(Text('Курс валют'))
async def exchange(message: types.Message, state: FSMContext):
    text = get_data()
    await state.set_state(ExchangeRate.text)
    await state.update_data(text=text)
    await message.reply(''.join(text[:25]), reply_markup=pagination(page=1))


@dp.callback_query(Text(startswith='page_'))
async def callbacks_page(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    action = data[1]
    page = int(data[2])
    if action == 'next':
        data_text = await state.get_data()
        text = data_text['text']
        new_page = page + 1
        second_item = 25 * new_page
        first_item = second_item - 25
        await callback.message.edit_text(''.join(text[first_item:second_item]), reply_markup=pagination(page=new_page))
    elif action == 'back':
        data_text = await state.get_data()
        text = data_text['text']
        new_page = page - 1
        second_item = 25 * new_page
        first_item = second_item - 25
        await callback.message.edit_text(''.join(text[first_item:second_item]), reply_markup=pagination(page=new_page))
    elif action == 'middle':
        await callback.answer(f'Page:{page}',)
    else:
        await callback.message.answer('Error! Send "/start".')