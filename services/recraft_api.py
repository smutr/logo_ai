import aiohttp
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

RECRAFT_API_URL = "https://external.api.recraft.ai/v1/images/generations"
RECRAFT_API_KEY = os.getenv("RECRAFT_API_KEY")



COLOR_MAP = {
    "orange": "orange",
    "blue": "blue",
    "green": "green",
    "violet": "violet",
    "black": "black",
    "white": "white",
    "yellow": "yellow",
    "pink": "pink",
    "random": "random"
}

SHAPE_MAP = {
    "square": "square",
    "circle": "circle",
    "text_icon": "abstract",      # или "abstract", если подразумевается такое
    "choice": "any",              # если пользователь выбрал "На свой выбор"
}


def get_color_en(color_code: str) -> str:
    code = color_code.replace("colors_", "")
    return COLOR_MAP.get(code, "random")

def get_shape_en(shape_code: str) -> str:
    code = shape_code.replace("shape_", "")
    return SHAPE_MAP.get(code, "any")




def build_prompt(
    description_en: str,
    color: Optional[str] = None,
    shape: Optional[str] = None,
    style: str = "minimal, clean, modern",
    background: str = "no background, transparent",
    include_text: bool = True,
    logo_type: str = "vector, flat design",
    mood: Optional[str] = None,
) -> str:
    """
    Формирует детальный промпт для Recraft logo generation с явным управлением формой.
    """
    parts = []

    # 1. Базовое описание логотипа
    base = f"Professional logo for {description_en}"
    parts.append(base)

    # 2. Цветовая палитра
    if color:
        parts.append(f"Use {color} color palette")

    # 3. Добавляем явное указание формы
    if shape == "circle":
        parts.append("Place the logo inside a solid circle. The logo must be fully contained within the circle, as a badge or round emblem.")
    elif shape == "square":
        parts.append("Place the logo inside a solid square. The logo must be fully contained within the square, as an emblem.")
    elif shape == "abstract":
        parts.append("The logo shape should be abstract, not geometric.")
    elif shape == "any" or shape is None:
        # Не добавляем ограничение по форме
        pass

    # 4. Тип логотипа и стиль
    if logo_type:
        parts.append(logo_type)
    if style:
        parts.append(style)

    # 5. Настроение (опционально)
    if mood:
        parts.append(f"with a {mood} mood")

    # 6. Текст в логотипе
    if include_text:
        parts.append("include brand name in a clear, readable font")
    else:
        parts.append("no text, symbol-only logo")

    # 7. Фон
    if background:
        parts.append(background)

    # 8. Общие требования для логотипов
    parts.append("high contrast, simple shapes, scalable, logo ready for branding")

    # Собираем всё в одну строку
    return ". ".join(parts) + "."




async def generate_logo(prompt: str, style: str, format_: str = "svg") -> tuple[str, int]:
    headers = {
        "Authorization": f"Bearer {RECRAFT_API_KEY}",
        "Content-Type": "application/json",
    }
    model = None

    if style in ["icon", "vector_illustration"]:
        model = "recraftv2"  # V2 обязателен для этих стилей
    else:
        model = "recraftv3"  # Все остальные стили — v3

    payload = {
        "prompt": prompt,
        "style": style,
        "format": format_,
        "model": model
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(RECRAFT_API_URL, headers=headers, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = data.get("data")
                if not results or not results[0].get("url"):
                    raise Exception(f"Recraft returned no image url: {data}")
                url = results[0]["url"]
                units_spent = data.get("credits", 99)
                return url, units_spent

            else:
                detail = await resp.text()
                raise Exception(f"Recraft gen failed! Code: {resp.status}, Detail: {detail}")

