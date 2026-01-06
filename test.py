
import requests


API_KEY='3mE9JEZ6Lq0OvjOG4SVhxWLAQO8QDQzswfZxoSvDsf0YtIlp3sf5qY631aGfKur2'


url = "https://external.api.recraft.ai/v1/images/generations"

payload = {
    "prompt": "picture of a bull boar",
    "style": "vector_illustration",
    "format": "svg"
}
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Raw text:", response.text)
if response.status_code == 200:
    print("JSON response:", response.json())
else:
    print("Ошибка! Код ответа:", response.status_code)
    print("Текст ответа:", response.text)

