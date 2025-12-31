# styles.py — вот примерно как это может выглядеть

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_styles_keyboard():
    """Клавиатура выбора стиля логотипа"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Минималистичный", callback_data="style_minimalist"),
                InlineKeyboardButton(text="🌈 Ярких цветов", callback_data="style_vibrant"),
            ],
            [
                InlineKeyboardButton(text="Геометрический 🔷", callback_data="style_geometric"),
                InlineKeyboardButton(text="Modern Tech 📱", callback_data="style_modern_tech")
            ],
            [
                InlineKeyboardButton(text="Классический 🎭", callback_data="style_classic"),
                InlineKeyboardButton(text="Абстрактный ✨", callback_data="style_abstract")
            ],
            [
                InlineKeyboardButton(text="Hand-drawn 🖌️", callback_data="style_hand"),
                InlineKeyboardButton(text="3D стиль 🎬", callback_data="style_3d")
            ],
            [
                InlineKeyboardButton(text="← Отмена", callback_data="cancel_generate"),
            ],
        ]
    )
    return keyboard
