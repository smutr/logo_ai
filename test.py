
import requests
import json


API_KEY='sk-2akrEBz3r66nEchKXaUghVOT14Bnx3cjOA57PiMEa70e72C6'

if not API_KEY:
    print("❌ ОШИБКА: API_KEY не найдена!")
    exit(1)

print(f"✅ API Key найдена!")

# ПРАВИЛЬНЫЙ ENDPOINT (используем ultra для качества)
url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

headers = {
    "authorization": f"Bearer {API_KEY}",
    "accept": "image/*"
}

data = {
    "prompt": "A logo of a plum-headed man riding a bicycle in a triangle shape.",
    "output_format": "png"
}

print("\n🎨 Генерируем логотип...")
print(f"📝 Промпт: {data['prompt']}")

try:
    # ⚠️ ВАЖНО: files={"none": ''} НУЖЕН!
    response = requests.post(
        url,
        headers=headers,
        files={"none": ''},  # ← КРИТИЧНО!
        data=data,
        timeout=60
    )

    print(f"\n📊 Статус ответа: {response.status_code}")

    if response.status_code == 200:
        with open("logo.png", "wb") as f:
            f.write(response.content)
        print("✅ УСПЕХ! Логотип создан!")
        print("📍 Файл сохранён: logo.png")
        print(f"📊 Размер: {len(response.content)} байт")
    else:
        print(f"❌ ОШИБКА: {response.status_code}")
        try:
            print(f"📝 Ответ: {response.json()}")
        except:
            print(f"📝 Ответ: {response.text}")

except Exception as e:
    print(f"❌ ОШИБКА подключения: {e}")