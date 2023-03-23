import requests

from aiogram import types
from aiogram import F
from loader import dp
from aiogram.filters.command import Command
from aiogram.filters import Text
from data import config
from keyboards.default.start_buttons import start_buttons_ru, start_buttons_en
from keyboards.inline.pagination import pagination
from keyboards.inline.language import language
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import List


class Language(StatesGroup):
    lang = State()


class ExchangeRate(StatesGroup):
    text = State()


def get_data() -> List[str]:
    response = requests.get(config.URL).json()
    currencies = response.get('conversion_rates')
    text = []
    for curr in currencies:
        text.append(f'\n{curr}: {currencies[curr]}')
    return text


@dp.message(Command('start'))
async def cmd_start(message: types.Message) -> None:
    await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())


@dp.message(F.text.in_(['Курс валют', 'Exchange rate']))
async def exchange(message: types.Message, state: FSMContext) -> None:
    text = get_data()
    await state.set_state(ExchangeRate.text)
    await state.update_data(text=text)
    await message.reply(''.join(text[:25]), reply_markup=pagination(page=1))


@dp.callback_query(Text(startswith='page_'))
async def callbacks_page(callback: types.CallbackQuery, state: FSMContext) -> None:
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


@dp.callback_query(Text(startswith='language_'))
async def language_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    data = callback.data.split('_')
    lang = data[1]
    await state.set_state(Language.lang)
    await state.update_data(lang=lang)
    if lang == 'ru':
        await callback.message.answer(f'Привет! Этот бот знает курс валют к доллару.'
                                      f'\n* Нажми кнопку "Курс валют" чтобы узнать нынешний курс.'
                                      f'\n* Нажми кнопку "Конвертер валют" чтобы конвертировать валюту.',
                                      reply_markup=start_buttons_ru())
        await callback.answer()
    elif lang == 'en':
        await callback.message.answer('en', reply_markup=start_buttons_en())
        await callback.answer()
