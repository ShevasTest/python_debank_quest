import requests

token = "7943346989:AAGMU0gZ5QSSu1Xy9aLJs1jvMSAdOE9Objg"
chat_id = "@testpydebank"  # chat_id должен быть в строковом формате
text = "Тестовое сообщение"

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    'chat_id': chat_id,
    'text': text
}

response = requests.post(url, data=payload)
print(response.json())  # Выводим ответ от API для проверки
