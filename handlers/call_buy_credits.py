from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.buy_credits_keyboard import get_buy_credits_keyboard
from keyboards.back import get_back_keyboard
router = Router()


@router.callback_query(lambda x: x.data == "buy_credits")
async def show_buy_credits(call: CallbackQuery):
    text = (
        "Покупка генераций\n\n"
        "1 генерация логотипа = 99 ₽.\n"
        "Чем больше пакет — тем дешевле одна генерация.\n\n"
        "Выберите нужное количество:"
    )
    await call.message.edit_text(
        text=text,
        reply_markup=get_buy_credits_keyboard(),
    )


PRICE_BY_CREDITS = {
    1: 99,
    2: 179,
    3: 249,
    5: 379,
    7: 499,
    10: 649,
    15: 899,
    20: 1099,
}




@router.callback_query(lambda x: x.data.startswith('buy_credits_'))
async def credits_number(call: CallbackQuery):
    credits = int(call.data.replace('buy_credits_', ''))
    await call.message.edit_text(text=f'Вы купили {credits} кредитов', reply_markup=get_back_keyboard())