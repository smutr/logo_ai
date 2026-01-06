from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_after_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧾 Еще генерации",
                    callback_data="buy_credits"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ В главное меню",
                    callback_data="back_to_menu"
                )
            ],
        ]
    )
