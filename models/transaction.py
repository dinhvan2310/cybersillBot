from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    id: int
    user_id: int
    type: str  # 'deposit' hoặc 'purchase'
    amount: float
    status: str  # 'pending', 'success', 'failed'
    created_at: datetime = None
    description: str = None 