from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def main():
    pass


def pagination(page=1) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardBuilder()
    if page == 1:
        inline_keyboard.button(text=f'{page}/7', callback_data=f'page_middle_{page}')
        inline_keyboard.button(text='>', callback_data=f'page_next_{page}')
    elif page == 7:
        inline_keyboard.button(text='<', callback_data=f'page_back_{page}')
        inline_keyboard.button(text=f'{page}/7', callback_data=f'page_middle_{page}')
    else:
        inline_keyboard.button(text='<', callback_data=f'page_back_{page}')
        inline_keyboard.button(text=f'{page}/7', callback_data=f'page_middle_{page}')
        inline_keyboard.button(text='>', callback_data=f'page_next_{page}')
    return inline_keyboard.as_markup()


if __name__ == '__main__':
    main()