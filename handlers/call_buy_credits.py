from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from keyboards.buy_credits_keyboard import get_buy_credits_keyboard
from keyboards.back import get_back_keyboard
from db.models import add_credit_user
from keyboards.confirm_payment_keyboard import get_confirm_payment_keyboard
from aiogram.types import LabeledPrice
from aiogram.types import PreCheckoutQuery

router = Router()


@router.callback_query(lambda x: x.data == "buy_credits")
async def show_buy_credits(call: CallbackQuery):
    text = (
        "Покупка генераций\n\n"
        "1 генерация логотипа = 100 ⭐ Telegram Stars.\n"
        "Чем больше пакет — тем выгоднее цена за одну генерацию!\n\n"
        "Выберите нужное количество, и Telegram предложит оплатить покупку звёздами.\n\n"
        "❓ *Что такое звёзды Telegram?*\n"
        "Это внутренняя валюта Telegram для быстрых и безопасных покупок "
        "цифровых товаров внутри приложений и ботов.\n\n"
        "💳 Если у вас нет звёзд — Telegram автоматически предложит их купить "
        "через App Store, Google Play или Fragment (crypto)."
    )

    await call.message.edit_text(
        text=text,
        reply_markup=get_buy_credits_keyboard(),
        parse_mode="Markdown"
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
from aiogram.types import LabeledPrice

@router.callback_query(lambda c: c.data.startswith('buy_credits_'))
async def pay_with_stars(call: CallbackQuery):
    credits = int(call.data.replace('buy_credits_', ''))
    stars_per_credit = 100      # допустим, 1 генерация = 100 звёзд (установи свою цену)
    amount = credits * stars_per_credit

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title="Покупка генераций LogoAI",
        description=f"{credits} генераций логотипа LogoAI",
        payload=f"logoai_stars_{credits}",
        provider_token="",     # фиксированное значение для звёзд,
        currency="XTR",             # ключ для звёзд!
        prices=[LabeledPrice(label=f"{credits} генераций", amount=amount)],  # amount — в звёздах!
        start_parameter="buy-credits"
    )


# назад к платежам
@router.callback_query(F.data == "back_to_buy_credits")
async def back_to_buy_credits(call: CallbackQuery):
    await call.message.edit_text(
        "Выберите пакет кредитов:",
        reply_markup=get_buy_credits_keyboard()
    )


# Подтвердить платеж
@router.message()
async def payment_handler(message: Message):
    # Обрабатываем только сообщения с успешной оплатой
    if not message.successful_payment:
        return

    payload = message.successful_payment.invoice_payload

    # Наши платежи за кредиты помечаем как "logoai_stars_<число>"
    if payload.startswith("logoai_stars_"):
        credits = int(payload.split("_")[-1])

        # Начисляем кредиты пользователю
        await add_credit_user(message.from_user.id, credits)

        await message.answer(
            "✅ Спасибо за оплату!\n\n"
            f"Вам начислено {credits} генераций "
            "(оплачено через Telegram Stars).\n\n"
            "Вы можете использовать генерации в любой момент "
            "для создания логотипа.\n"
            "Ваш баланс всегда доступен в профиле."
        , reply_markup=get_buy_credits_keyboard())


@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
