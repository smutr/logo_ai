from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states.generate import GenerateStates
from keyboards.generate.styles import get_styles_keyboard
from keyboards.generate.colors import get_colors_keyboard
from keyboards.generate.shapes import get_shapes_keyboard
from keyboards.main_menu import get_main_keyboard
from keyboards.back import get_back_keyboard
from db.models import User, get_or_create_user, try_decrement_generation
from services.recraft_api import build_prompt
from services.translator import TranslatorService
from services.recraft_api import generate_logo
from db.models import save_generation

router = Router()


@router.callback_query(F.data == 'start_generate')
async def call_start_generate(call: CallbackQuery, state: FSMContext):
    user, status = await try_decrement_generation(call.from_user.id)
    # Следует продолжить с этого места и привинтить новую функцию из модели

    if user is None:
        user = await get_or_create_user(call.from_user.id, call.from_user.username or "Undefined")

    if status in ('free', 'paid'):
        await state.set_state(GenerateStates.waiting_description)
        await call.message.edit_text(text="📝 Опиши свой бренд одной строкой\n\nПример: кофейня с современным дизайном")


    else:
        await call.message.edit_text(text="❌ У тебя нет кредитов!\n\n💰 Купи кредиты в меню", reply_markup=get_back_keyboard())


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






# Функция скачивает файл по ссылке и отправляет в чат
# async def send_logo_document(chat_id, url, bot, ext="svg"):
#     # Скачиваем файл по url локально
#     filename = f"logo.{ext}"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             data = await resp.read()
#             with open(filename, "wb") as f:
#                 f.write(data)
#     file = FSInputFile(filename)
#     # Отправляем как документ, чтобы не портилось качество
#     await bot.send_document(chat_id, file, caption="Ваш логотип готов!")




@router.callback_query(F.data.startswith('shape_'))
async def process_shape(call: CallbackQuery, state: FSMContext):
    shape = call.data.replace('shape_', '')
    await state.update_data(shape=shape)

    data = await state.get_data()
    await state.clear()

    text_params = (
        "✅ Готово! Вот твои параметры:\n\n"
        f"📝 Описание: {data['description']}\n"
        f"🎨 Стиль: {data['style']}\n"
        f"🎨 Цвет: {data['color']}\n"
        f"📐 Форма: {data['shape']}\n\n"
        "⏳ Генерирую логотип..."
    )

    await call.message.edit_text(text=text_params)

    translator = TranslatorService()
    description_en = await translator.translate_ru_to_en(text=data['description'])

    # Маппинг цвета и формы на английский
    color_en = data['color']
    shape_en = data['shape']

    prompt = build_prompt(
        description_en=description_en,
        color=color_en,
        shape=shape_en,
        style=data['style'],
    )

    try:
        url, units_spent = await generate_logo(prompt=prompt, style=data['style'])
        user = await get_or_create_user(call.from_user.id, call.from_user.username or "Unknown")

        await save_generation(
            user_id=user.id,
            prompt=prompt,
            style=data["style"],
            url=url,
            units=units_spent,
        )

        result_text = (
            "✅ Ваш логотип готов!\n\n"
            f"🔗 [Скачать SVG (векторный логотип)]({url})\n\n"
            "SVG — исходный векторный формат. Откройте в браузере или редакторе (Figma, Illustrator).\n"
            "Если нужен PNG/JPG или предпросмотр — напишите нам или воспользуйтесь онлайн-конвертером.\n\n"
            "Хотите получить новый логотип? Просто начните генерацию с новыми параметрами или используйте меню."
        )

        await call.message.answer(
            text=result_text,
            parse_mode="Markdown",
        )
    except Exception as e:
        error_text = (
            f"❌ Ошибка генерации логотипа: {e}\n\n"
            "Попробуйте снова или измените параметры."
        )
        await call.message.answer(
            text=error_text,
            reply_markup=get_main_keyboard(),
        )





@router.callback_query(F.data == 'cancel_generate')
async def process_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "🎨 Добро пожаловать в LogoAI!\n\n"
        "Я помогу создать идеальный логотип для твоего бренда за минуты.\n\n"
        "Твой баланс: 💎 3 генерации (Free trial)",
        reply_markup=get_main_keyboard()
    )
