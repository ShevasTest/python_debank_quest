# api.py

import asyncio
from playwright.async_api import async_playwright
import requests
from models import QuestResponse
from utils import create_quest_url

async def get_debank_quest_api_headers() -> tuple:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        headers = {}

        async def on_request(request):
            if request.url.startswith("https://api.debank.com/quest/list"):
                headers['x-api-nonce'] = request.headers.get('x-api-nonce', '')
                headers['x-api-sign'] = request.headers.get('x-api-sign', '')
                headers['x-api-ts'] = request.headers.get('x-api-ts', '')

        page.on("request", on_request)
        await page.goto("https://debank.com/quest")
        await page.wait_for_selector('div[class^="QuestCard_title__"]')
        await browser.close()

    return headers.get('x-api-nonce', ''), headers.get('x-api-sign', ''), headers.get('x-api-ts', '')

def fetch_quest_data(api_url: str, headers: dict) -> QuestResponse:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return QuestResponse.parse_obj(response.json())
