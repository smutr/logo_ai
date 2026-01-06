from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_styles_keyboard():
    """Клавиатура выбора стиля логотипа (реальные стили Recraft)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖋️ Векторная (SVG)", callback_data="style_vector_illustration"),
                InlineKeyboardButton(text="🔲 Иконка", callback_data="style_icon"),
            ],
            [
                InlineKeyboardButton(text="🖼️ Иллюстрация", callback_data="style_digital_illustration"),

            ],
            [
                InlineKeyboardButton(text="← Отмена", callback_data="cancel_generate"),
            ],
        ]
    )
    return keyboard
