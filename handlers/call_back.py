from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main_menu import get_main_keyboard

router = Router()


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text(text="🎨 Добро пожаловать в LogoAI!\n\n"
                                      "Я помогу создать идеальный логотип для твоего бренда за минуты.\n\n"
                                      "Твой баланс: 💎 3 генерации (Free trial)", reply_markup=get_main_keyboard())
