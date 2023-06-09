import requests

from typing import Any, Dict
from data import config
from loader import dp
from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.default.start_buttons import start_buttons_ru, start_buttons_en, cancel_button_ru, cancel_button_en
from keyboards.inline.language import language
from handlers.handlers import Language


class Converter(StatesGroup):
    first_value = State()
    quantity = State()
    second_value = State()


currencies = ['USD', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
              'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP',
              'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD',
              'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG',
              'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR',
              'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA',
              'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK',
              'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF',
              'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL',
              'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES',
              'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']


@dp.message(F.text.in_(['Конвертер валют', 'Currency converter']))
async def converter(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    if 'lang' in data:
        lang = data['lang']
    else:
        lang = None
    await state.set_state(Converter.first_value)
    if lang == 'ru':
        await message.answer(f'Выберите валюту, которую хотите конвертировать.\nПример: \"USD\".',
                             reply_markup=cancel_button_ru())
    elif lang == 'en':
        await message.answer(f'Select the currency you want to convert.\nExample: \"USD\".',
                             reply_markup=cancel_button_en())
    else:
        await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())


@dp.message(F.text.in_(['Отмена', 'Cancel']))
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    data = await state.get_data()
    if 'lang' in data:
        lang = data['lang']
    else:
        lang = None
    await state.clear()
    if lang == 'ru':
        await state.set_state(Language.lang)
        await state.update_data(lang=lang)
        await message.answer('Отменено', reply_markup=start_buttons_ru())
    elif lang == 'en':
        await state.set_state(Language.lang)
        await state.update_data(lang=lang)
        await message.answer('Cancelled', reply_markup=start_buttons_en())
    else:
        await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())


@dp.message(Converter.first_value)
async def first(message: types.Message, state: FSMContext) -> None:
    if message.text.upper() in currencies:
        await state.update_data(first_value=message.text.upper())
        await state.set_state(Converter.quantity)
        data = await state.get_data()
        if 'lang' in data:
            lang = data['lang']
        else:
            lang = None
        if lang == 'ru':
            await message.answer('Отправьте количество валюты.\nПример: 13.44')
        elif lang == 'en':
            await message.answer('Enter the quantity.\nExample: 13.44')
        else:
            await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())
    else:
        await state.set_state(Converter.first_value)
        await message.answer(f'Error: InvalidCurrency. Try again.')


@dp.message(Converter.quantity)
async def enter_quantity(message: types.Message, state: FSMContext) -> None:
    message_quantity = []
    data = await state.get_data()
    if 'lang' in data:
        lang = data['lang']
    else:
        lang = None
    for i in message.text:
        if i.isdigit():
            message_quantity.append(i)
        elif i == '.':
            message_quantity.append(i)
        else:
            pass
    result = ''.join(message_quantity)
    if result == '':
        await state.set_state(Converter.quantity)
        if lang == 'ru':
            await message.answer('Сообщение должно быть числом.\nПример: 13.44.')
        elif lang == 'en':
            await message.answer('The message must be a number.\nExample: 13.44.')
        else:
            await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())
    else:
        await state.update_data(quantity=float(result))
        await state.set_state(Converter.second_value)
        if lang == 'ru':
            await message.answer('Выберите валюту, которую хотите получить.\nПример: \"EUR\".')
        elif lang == 'en':
            await message.answer('Choose the currency you will receive.\nExample: \"EUR\".')
        else:
            await message.answer('Choose a language.\nВыберите язык.', reply_markup=language())


@dp.message(Converter.second_value)
async def second(message: types.Message, state: FSMContext) -> None:
    if message.text.upper() in currencies:
        data = await state.update_data(second_value=message.text.upper())
        lang = data['lang']
        await state.clear()
        await state.set_state(Language.lang)
        await state.update_data(lang=lang)
        await converted(message=message, data=data, lang=lang)
    else:
        await state.set_state(Converter.second_value)
        await message.answer(f'Error: InvalidCurrency. Try again.')


async def converted(message: types.Message, data: Dict[str, Any], lang: str) -> None:
    text = message.text.upper()
    first_curr = data['first_value']
    response = requests.get(config.URL).json()
    from_curr = response.get('conversion_rates')[first_curr]
    to_curr = response.get('conversion_rates')[text]
    quantity = data['quantity']
    if lang == 'en':
        await message.answer(f'Converted: {round((to_curr / from_curr) * float(quantity), 2)} {text}',
                             reply_markup=start_buttons_en())
    elif lang == 'ru':
        await message.answer(f'Конвертировано: {round((to_curr / from_curr) * float(quantity), 2)} {text}',
                             reply_markup=start_buttons_ru())
