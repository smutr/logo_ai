from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards.buy_credits_keyboard import get_buy_credits_keyboard
from keyboards.back import get_back_keyboard
from db.models import add_credit_user
from keyboards.confirm_payment_keyboard import get_confirm_payment_keyboard

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



# купить кредиты
@router.callback_query(lambda x: x.data.startswith('buy_credits_'))
async def credits_number(call: CallbackQuery):
    credits = int(call.data.replace('buy_credits_', ''))

    await call.message.edit_text(
        text=(
            f"Вы выбрали пакет на <b>{credits}</b> кредит(ов).\n\n"
            "Каждый кредит — это одна генерация логотипа в высоком качестве.\n\n"
            "Подтвердите покупку:"
        ),
        reply_markup=get_confirm_payment_keyboard(credits),
        parse_mode=ParseMode.HTML
    )

# назад к платежам
@router.callback_query(F.data == "back_to_buy_credits")
async def back_to_buy_credits(call: CallbackQuery):
    await call.message.edit_text(
        "Выберите пакет кредитов:",
        reply_markup=get_buy_credits_keyboard()
    )


# Подтвердить платеж
@router.callback_query(F.data.startswith('pay_credits_'))
async def pay_credits(call: CallbackQuery):
    credits = int(call.data.replace('pay_credits_', ""))
    await add_credit_user(call.from_user.id, credits)
    await call.message.edit_text(
        text=f'✅ Спасибо! Вам начислено {credits} платных генераций.',
    reply_markup=get_back_keyboard())
