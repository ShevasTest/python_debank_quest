# telegram_bot.py

import requests
import json

class InlineKeyboardButton:
    def __init__(self, text: str, url: str):
        self.text = text
        self.url = url

    def to_dict(self):
        return {"text": self.text, "url": self.url}

class InlineKeyboardMarkup:
    def __init__(self, buttons: list):
        self.inline_keyboard = buttons

    def to_dict(self):
        return {"inline_keyboard": self.inline_keyboard}

def send_message(bot_token: str, chat_id: str, text: str, button_text: str, button_url: str):
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    button = InlineKeyboardButton(text=button_text, url=button_url)
    keyboard = InlineKeyboardMarkup([[button.to_dict()]])
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": keyboard.to_dict()
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
