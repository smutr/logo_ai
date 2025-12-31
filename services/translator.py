import aiohttp

class TranslatorService:
    def __init__(self):
        self.url = 'https://api.mymemory.translated.net/get'

    async def translate_ru_to_en(self, text: str) -> str:
        """Переводит с русского на английский"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params={
                    "q": text,
                    "langpair": "ru|en"
                }
            ) as response:
                data = await response.json()
                return data["responseData"]["translatedText"]
