from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_keyboard
from db.models import get_or_create_user

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )
    await message.answer(
        "🎨 Добро пожаловать в LogoAI!\n\n"
        "Я помогу создать идеальный логотип для твоего бренда за минуты.\n\n"
        "Твой баланс: 💎 1 генерация (One trial)",
        reply_markup=get_main_keyboard()
    )
