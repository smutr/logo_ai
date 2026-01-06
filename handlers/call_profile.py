from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.back import get_back_keyboard
from db.models import get_or_create_user, count_user_logos

router = Router()


@router.callback_query(lambda x: x.data == "profile")
async def show_profile(call: CallbackQuery):
    user = await get_or_create_user(
        call.from_user.id,
        call.from_user.username or "Без имени",
    )
    count_logos = await count_user_logos(user.id)

    text = (
        "👤 *Профиль пользователя*\n"
        "\n"
        f"🆔 Username: `{user.username}`\n"
        f"🎁 Бесплатные генерации: *{user.free_generations_left}*\n"
        f"💳 Платные генерации: *{user.paid_generations}*\n"
        f"🖼 Всего логотипов: *{count_logos}*\n"
    )

    await call.message.edit_text(
        text=text,
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown",
    )


