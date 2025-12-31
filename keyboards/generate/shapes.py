from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_shapes_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬜ Квадратный ", callback_data="shape_square"),
                InlineKeyboardButton(text="⭕ Круглый", callback_data="shape_circle")
            ],
            [
                InlineKeyboardButton(text="🔷 Абстрактный", callback_data="shape_text_icon"),
                InlineKeyboardButton(text="На свой выбор", callback_data="shape_choice")
            ],
            [
                InlineKeyboardButton(text="← Отмена", callback_data="cancel_generate")
            ],

        ]
    )
