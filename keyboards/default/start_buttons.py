from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram import types


def main():
    pass


def start_buttons_ru() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Курс валют'))
    keyboard.add(types.KeyboardButton(text='Конвертер валют'))
    return keyboard.as_markup(resize_keyboard=True)


def start_buttons_en() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Exchange rate'))
    keyboard.add(types.KeyboardButton(text='Currency converter'))
    return keyboard.as_markup(resize_keyboard=True)


def cancel_button_ru() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Отмена'))
    return keyboard.as_markup(resize_keyboard=True)


def cancel_button_en() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Cancel'))
    return keyboard.as_markup(resize_keyboard=True)


if __name__ == '__main__':
    main()