from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from aiogram import types


def main():
    pass


def start_buttons() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Exchange rate'))
    keyboard.add(types.KeyboardButton(text='Currency converter'))
    return keyboard.as_markup(resize_keyboard=True)


def cancel_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(types.KeyboardButton(text='Cancel'))
    return keyboard.as_markup(resize_keyboard=True)


if __name__ == '__main__':
    main()