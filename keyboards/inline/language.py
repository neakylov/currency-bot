from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def language() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🇷🇺', callback_data=f'language_ru')
    builder.button(text='🇬🇧', callback_data=f'language_en')
    return builder.as_markup()