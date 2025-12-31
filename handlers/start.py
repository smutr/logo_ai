from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🎨 Добро пожаловать в LogoAI!\n\n"
        "Я помогу создать идеальный логотип для твоего бренда за минуты.\n\n"
        "Твой баланс: 💎 3 генерации (Free trial)",
        reply_markup=get_main_keyboard()
    )
