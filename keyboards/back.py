from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='← Назад', callback_data='back_to_menu')]
        ]
    )
