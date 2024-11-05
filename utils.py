# utils.py

import os
from urllib.parse import urlencode

def create_quest_url(quest_id: int) -> str:
    r = "102696"
    base_url = "https://debank.com/stream/"
    return f"{base_url}{quest_id}?{urlencode({'r': r})}"
