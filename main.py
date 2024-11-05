import asyncio
import os
import time
import logging
from dotenv import load_dotenv
from flask import Flask, Response
from api import fetch_quest_data, get_debank_quest_api_headers
from telegram_bot import send_message
from models import QuestResponse
from utils import create_quest_url

# Загрузка переменных окружения
load_dotenv()

API_URL = os.getenv("API_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_IDS = ["@ProfiT_Mafia_Chat", "@TestnetProfitMafia"]  # Нужные чаты
PORT = os.getenv("PORT", "8080")
RETRY_INTERVAL = 60  

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Flask приложения для health check
app = Flask(__name__)

@app.route('/health')
def health_check():
    return Response("OK", status=200)

def init_seen_quests(api_url: str, headers: dict) -> dict:
    logger.info("Инициализация просмотренных квестов...")
    seen_quest_ids = {}
    
    try:
        quest_response = fetch_quest_data(api_url, headers)
        for quest in quest_response.data.quests:
            quest_id = quest.article.id
            seen_quest_ids[quest_id] = {}
    except Exception as e:
        logger.error(f"Ошибка инициализации квестов: {e}")
        
    return seen_quest_ids

def process_quests(api_url: str, headers: dict, bot_token: str, channel_ids: list, seen_quest_ids: dict):
    try:
        quest_response = fetch_quest_data(api_url, headers)
        for quest in quest_response.data.quests:
            quest_id = quest.article.id
            if quest_id not in seen_quest_ids:
                quest_name = quest.article.quest.name
                xp = quest.article.quest.unit_xp
                message = f"[New Quest: {quest_name}]({create_quest_url(quest_id)})\n\n---------------------------------\n\n" \
                          f"[🔥 Все для мульти-аккаунтов](https://t.me/ProfiT_Mafia/82)\n\n" \
                          f"[💰 Карта Казахстана](https://t.me/ProfiT_Mafia/770)\n\n" \
                          f"💻 DEBANK QUEST BOT | PROFIT MAFIA"
                button_text = f"View Quest {xp} XP"
                button_url = create_quest_url(quest_id)
                
                for channel_id in channel_ids:
                    send_message(bot_token, channel_id, message, button_text, button_url)
                
                seen_quest_ids[quest_id] = {}
                logger.info(f"Отправлено сообщение о новом квесте: {quest_name}")
    except Exception as e:
        logger.error(f"Ошибка обработки квестов: {e}")

def run_http_server():
    app.run(host='0.0.0.0', port=int(PORT))

def main():
    # Получение заголовков API
    headers = {}
    try:
        api_nonce, api_sign, api_ts = asyncio.run(get_debank_quest_api_headers())
        headers = {
            "x-api-nonce": api_nonce,
            "x-api-sign": api_sign,
            "x-api-ts": api_ts,
            "accept": "*/*",
            "accept-language": "en,th-TH;q=0.9,th;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://debank.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://debank.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "source": "web",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-api-ver": "v2"
        }
    except Exception as e:
        logger.error(f"Ошибка получения заголовков API: {e}")
        return

    # Инициализация просмотренных квестов
    seen_quest_ids = init_seen_quests(API_URL, headers)

    # Запуск HTTP сервера в отдельном потоке
    import threading
    server_thread = threading.Thread(target=run_http_server, daemon=True)
    server_thread.start()

    round_counter = 0
    while True:
        logger.info(f"Запуск раунда {round_counter}...")
        process_quests(API_URL, headers, TELEGRAM_BOT_TOKEN, CHANNEL_IDS, seen_quest_ids)
        time.sleep(RETRY_INTERVAL)
        round_counter += 1

if __name__ == "__main__":
    main()
