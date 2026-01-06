from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton





def get_buy_credits_keyboard() -> InlineKeyboardMarkup:
    plans = [
        {"credits": 1, "price": 99, "label": "На пробу"},
        {"credits": 2, "price": 179, "label": "Мини"},          # ~89 ₽
        {"credits": 3, "price": 249, "label": "Старт"},         # ~83 ₽
        {"credits": 5, "price": 379, "label": "Популярный ⭐"},  # ~76 ₽
        {"credits": 7, "price": 499, "label": "Выгодно 🔥"},    # ~71 ₽
        {"credits": 10, "price": 649, "label": "Профи"},        # ~65 ₽
        {"credits": 15, "price": 899, "label": "Студия"},       # ~60 ₽
        {"credits": 20, "price": 1099, "label": "Агентство"},   # ~55 ₽
    ]

    buttons = []
    row = []
    for i, plan in enumerate(plans, 1):
        text = f"{plan['credits']} — {plan['price']} ₽"
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f"buy_credits_{plan['credits']}"
            )
        )
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(text="ℹ️ Подробнее о генерациях", callback_data="credits_info")
    ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
