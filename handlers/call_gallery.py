from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

from db.models import get_user_logos, get_or_create_user
from keyboards.back import get_back_keyboard
import aiohttp
from sqlalchemy import update


router = Router()


@router.callback_query(lambda c: c.data == "gallery")
async def show_gallery(call: CallbackQuery):
    user = await get_or_create_user(
        telegram_id=call.from_user.id,
        username=call.from_user.username or "Unknown",
    )

    logos = await get_user_logos(user.id, limit=20)  # чуть больше для фильтрации

    if not logos:
        await call.message.answer(
            "📁 <b>Ваша галерея пока пуста.</b>\n"
            "Создайте свой первый логотип через главное меню ✨",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard(),
        )
        return

    valid_logos = []
    async with aiohttp.ClientSession() as session:
        async with async_session_maker() as db:
            for gen in logos:
                try:
                    async with session.head(gen.url, timeout=5) as resp:
                        if resp.status == 200:
                            valid_logos.append(gen)
                        else:
                            # помечаем как неактивный
                            await db.execute(
                                update(LogoGeneration)
                                .where(LogoGeneration.id == gen.id)
                                .values(is_active=False)
                            )
                except Exception:
                    await db.execute(
                        update(LogoGeneration)
                        .where(LogoGeneration.id == gen.id)
                        .values(is_active=False)
                    )
            await db.commit()

    if not valid_logos:
        await call.message.answer(
            "📁 <b>Все старые логотипы более недоступны.</b>\n"
            "Создайте новые в генераторе ✨",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard(),
        )
        return

    lines = [
        "🖼 <b>Ваши последние логотипы</b>\n",
        f"Найдено: <b>{len(valid_logos)}</b>\n",
    ]

    for i, gen in enumerate(valid_logos[:5], 1):
        date_str = gen.created_at.strftime("%d.%m.%Y %H:%M")
        style = gen.style.replace("_", " ").title()
        lines.append(
            "<b>────────────</b>\n"
            f"<b>{i}.</b> {date_str}\n"
            f"Тип: <b>{style}</b>\n"
            f'<a href="{gen.url}">🔗 Открыть SVG</a>'
        )

    gallery_text = "\n".join(lines)

    await call.message.answer(
        gallery_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=get_back_keyboard(),
    )