from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def get_buy_credits_keyboard() -> InlineKeyboardMarkup:
    # цены уже в ⭐, а не в рублях
    plans = [
        {"credits": 1, "price": 100, "label": "На пробу"},
        {"credits": 2, "price": 190, "label": "Мини"},          # ~95 ⭐
        {"credits": 3, "price": 270, "label": "Старт"},         # ~90 ⭐
        {"credits": 5, "price": 430, "label": "Популярный ⭐"},  # ~86 ⭐
        {"credits": 7, "price": 560, "label": "Выгодно 🔥"},    # ~80 ⭐
        {"credits": 10, "price": 750, "label": "Профи"},        # ~75 ⭐
        {"credits": 15, "price": 1050, "label": "Студия"},      # ~70 ⭐
        {"credits": 20, "price": 1300, "label": "Агентство"},   # ~65 ⭐
    ]

    buttons = []
    row = []

    for i, plan in enumerate(plans, 1):
        text = f"{plan['credits']} ген. — {plan['price']} ⭐"
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f"buy_credits_{plan['credits']}",
            )
        )
        if i % 2 == 0:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text="ℹ️ Подробнее о генерациях",
            callback_data="credits_info",
        )
    ])
    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_to_menu",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

