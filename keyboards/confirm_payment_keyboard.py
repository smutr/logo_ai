from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirm_payment_keyboard(credits: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💳 Оплатить {credits} кредит(ов)",
                    callback_data=f"pay_credits_{credits}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к выбору пакетов",
                    callback_data="back_to_buy_credits",
                )
            ]
        ]
    )
