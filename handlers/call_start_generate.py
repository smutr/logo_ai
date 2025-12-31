from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.generate import GenerateStates
from keyboards.generate.styles import get_styles_keyboard
from keyboards.generate.colors import get_colors_keyboard
from keyboards.generate.shapes import get_shapes_keyboard
from keyboards.main_menu import get_main_keyboard

router = Router()


@router.callback_query(F.data == 'start_generate')
async def call_start_generate(call: CallbackQuery, state: FSMContext):
    balance = 3

    if balance > 0:
        await state.set_state(GenerateStates.waiting_description)
        await call.message.edit_text(text="📝 Опиши свой бренд одной строкой\n\nПример: кофейня с современным дизайном")


    else:
        await call.message.edit_text(text="❌ У тебя нет кредитов!\n\n💰 Купи кредиты в меню")


@router.message(GenerateStates.waiting_description)
async def process_description(message: Message, state: FSMContext):
    """Обработка описания бренда"""

    await state.update_data(description=message.text)

    await state.set_state(GenerateStates.waiting_style)

    await message.answer(
        text="🎨 Выбери стиль логотипа:",
        reply_markup=get_styles_keyboard()
    )


@router.callback_query(F.data.startswith('style_'))
async def process_style(call: CallbackQuery, state: FSMContext):
    style = call.data.replace('style_', '')

    await state.update_data(style=style)
    await state.set_state(GenerateStates.waiting_color)
    await call.message.edit_text(text='🎨 Выбери цвет логотипа:', reply_markup=get_colors_keyboard())


@router.callback_query(F.data.startswith("colors_"))
async def process_color(call: CallbackQuery, state: FSMContext):
    color = call.data.replace('colors_', "")
    await state.update_data(color=color)
    await state.set_state(GenerateStates.waiting_shape)
    await call.message.edit_text(text='📐 Выбери форму логотипа:', reply_markup=get_shapes_keyboard())


@router.callback_query(F.data.startswith('shape_'))
async def process_shape(call: CallbackQuery, state: FSMContext):
    shape = call.data.replace('shape_', '')
    await state.update_data(shape=shape)

    data = await state.get_data()
    await state.clear()

    await call.message.edit_text(text=f"""✅ Готово! Вот твои параметры:

📝 Описание: {data['description']}
🎨 Стиль: {data['style']}
🎨 Цвет: {data['color']}
📐 Форма: {data['shape']}

⏳ Начинаю генерацию...
""")


@router.callback_query(F.data == 'cancel_generate')
async def process_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "🎨 Добро пожаловать в LogoAI!\n\n"
        "Я помогу создать идеальный логотип для твоего бренда за минуты.\n\n"
        "Твой баланс: 💎 3 генерации (Free trial)",
        reply_markup=get_main_keyboard()
    )

