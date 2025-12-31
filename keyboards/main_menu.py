from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    """Главное меню с кнопками"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Начать генерацию", callback_data="start_generate")],
            [InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")],
            [InlineKeyboardButton(text="🖼️ Галерея", callback_data="gallery")],
            [InlineKeyboardButton(text="💰 Купить кредиты", callback_data="buy_credits")],
            [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")],
        ]
    )
    return keyboard
