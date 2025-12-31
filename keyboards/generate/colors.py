
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_colors_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟠 Оранжевый", callback_data="colors_orange"),
                InlineKeyboardButton(text="🔵 Синий", callback_data="colors_blue")
            ],
            [
                InlineKeyboardButton(text="🟢 Зелёный", callback_data="colors_green"),
                InlineKeyboardButton(text="🟣 Фиолетовый", callback_data="colors_violet")
            ],
            [
                InlineKeyboardButton(text="⚫ Чёрный", callback_data="colors_black"),
                InlineKeyboardButton(text="⚪ Белый", callback_data="colors_white")
            ],
            [
                InlineKeyboardButton(text="🟡 Жёлтый", callback_data="colors_yellow"),
                InlineKeyboardButton(text="🩷 Розовый", callback_data="colors_pink")
            ],
            [
                InlineKeyboardButton(text="🎲 Random", callback_data="colors_random")
            ],
            [
                InlineKeyboardButton(text="← Отмена", callback_data="cancel_generate")
            ]
        ]
    )