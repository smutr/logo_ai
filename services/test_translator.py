import asyncio
import time
from services.translator import TranslatorService

# Список фраз для теста (разные тематики)
TEST_PHRASES = [
    "Кофейня с минималистичным дизайном",
    "Строительная компания Надежный Дом",
    "Салон красоты для собак и кошек",
    "Магазин автозапчастей Форсаж",
    "Студия веб-разработки и дизайна",
    "Доставка суши и роллов за 30 минут",
    "Элитная недвижимость в центре Москвы",
    "Онлайн школа английского языка",
    "Барбершоп с брутальным интерьером",
    "Детский магазин игрушек Радуга"
]


async def translate_phrase(service, text, index):
    """Переводит одну фразу и замеряет время"""
    start_time = time.time()
    try:
        result = await service.translate_ru_to_en(text)
        duration = time.time() - start_time
        return {
            "index": index,
            "original": text,
            "translated": result,
            "time": duration,
            "status": "✅ OK"
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "index": index,
            "original": text,
            "translated": str(e),
            "time": duration,
            "status": "❌ ERROR"
        }


async def run_load_test():
    print(f"🚀 Запуск нагрузочного теста на {len(TEST_PHRASES)} запросов...")
    print("-" * 60)

    translator = TranslatorService()
    start_total = time.time()

    # Создаем задачи для всех фраз ОДНОВРЕМЕННО
    tasks = [translate_phrase(translator, text, i) for i, text in enumerate(TEST_PHRASES)]

    # Запускаем все сразу
    results = await asyncio.gather(*tasks)

    end_total = time.time()
    total_time = end_total - start_total

    # Вывод результатов
    print(f"{'#':<3} | {'Время (сек)':<12} | {'Статус':<8} | {'Оригинал':<35} | {'Перевод'}")
    print("-" * 100)

    success_count = 0
    total_request_time = 0

    for res in results:
        if res["status"] == "✅ OK":
            success_count += 1
            total_request_time += res["time"]

        print(
            f"{res['index']:<3} | {res['time']:.4f}       | {res['status']:<8} | {res['original']:<35} | {res['translated']}")

    print("-" * 100)
    print(f"\n📊 ИТОГИ:")
    print(f"Всего запросов: {len(TEST_PHRASES)}")
    print(f"Успешно: {success_count}")
    print(f"Ошибок: {len(TEST_PHRASES) - success_count}")
    print(f"Общее время выполнения: {total_time:.2f} сек")
    if success_count > 0:
        print(f"Среднее время на запрос: {total_request_time / success_count:.4f} сек")
    else:
        print("Среднее время: N/A")


if __name__ == "__main__":
    asyncio.run(run_load_test())
