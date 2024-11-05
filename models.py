# models.py

from typing import List, Optional
from pydantic import BaseModel

class QuestResponse(BaseModel):
    data: 'Data'

class Data(BaseModel):
    quests: List['Quest']

class Quest(BaseModel):
    article: 'Article'

class Article(BaseModel):
    id: int
    quest: 'QuestDetails'

class QuestDetails(BaseModel):
    name: str
    unit_xp: int

class Creator(BaseModel):
    avatar_thumbnail_url: str
    avatar_url: str
    banner_thumbnail_url: str
    banner_url: str
    create_at: float
    follower_count: int
    id: int
    initial_price: int
    intro: str
    is_following: bool
    is_muted: bool
    is_premium: bool
    name: str
    site_id: str
    slug: str
    tvf: float
    twitter_id: str
    twitter_id_verified: bool
    type: str
    uncharged_offer_count: int
    uncharged_offer_value: int
    verify_status: int

class URL(BaseModel):
    display_url: str
    indices: List[int]
    raw_string: str
    url: str

class Entities(BaseModel):
    channels: List[Optional[str]]
    mentions: List[Optional[str]]
    tags: List[Optional[str]]
    url: List[URL]

class Action(BaseModel):
    create_at: float
    data: dict
    id: int
    is_verified: bool
    quest_id: int
    task_id: int
    type: str
    unit_xp: int

class Draw(BaseModel):
    block_id: Optional[str]
    create_at: float
    duration: int
    finish_at: float
    has_permission: bool
    id: int
    is_settled: bool
    join_count: int
    operations: Optional[str]
    permissions: Optional[str]
    prize_count: int
    prize_custom: Optional[str]
    prize_custom_distribution: Optional[str]
    prize_value: int
    settled_at: Optional[str]
    winner_count: Optional[str]
