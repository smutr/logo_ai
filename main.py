
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.methods import SendMessage
import asyncio
from config import BOT_TOKEN
from handlers import routers
from utils.loggers import logger




logger.info("🚀 Запуск LogoAI бота...")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



async def main():
    logger.info("📡 Подключение обработчиков...")

    for router in routers:
        dp.include_router(router)

    logger.info("✅ Бот запущен и слушает сообщения")
    await dp.start_polling(bot)





if __name__ == "__main__":
    asyncio.run(main())

