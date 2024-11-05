import requests

token = "7943346989:AAGMU0gZ5QSSu1Xy9aLJs1jvMSAdOE9Objg"
chat_ids = ["@testpythonchatquest", "@test2quest"] 
text = "Тестовое сообщение"

url = f"https://api.telegram.org/bot{token}/sendMessage"

# Отправка сообщения в каждый указанный чат
for chat_id in chat_ids:
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    print(response.json())
