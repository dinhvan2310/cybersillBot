from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    username: str
    email: str = None
    language: str = "en"  # Trường ngôn ngữ, mặc định là tiếng Anh
    created_at: datetime = None 