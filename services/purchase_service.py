import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class PurchaseService:
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    group_chat_id TEXT,
                    bot_token TEXT,
                    purchase_time TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_purchase(self, user_id: int, product_id: int, group_chat_id: Optional[str] = None, bot_token: Optional[str] = None) -> int:
        purchase_time = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO purchases (user_id, product_id, group_chat_id, bot_token, purchase_time) VALUES (?, ?, ?, ?, ?)',
                      (user_id, product_id, group_chat_id, bot_token, purchase_time))
            conn.commit()
            return c.lastrowid

    def get_purchases_by_user(self, user_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, user_id, product_id, group_chat_id, bot_token, purchase_time FROM purchases WHERE user_id = ?', (user_id,))
            rows = c.fetchall()
            return [
                {'id': row[0], 'user_id': row[1], 'product_id': row[2], 'group_chat_id': row[3], 'bot_token': row[4], 'purchase_time': row[5]}
                for row in rows
            ]

    def get_users_by_product(self, product_id: int) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, user_id, product_id, group_chat_id, bot_token, purchase_time FROM purchases WHERE product_id = ?', (product_id,))
            rows = c.fetchall()
            return [
                {'id': row[0], 'user_id': row[1], 'product_id': row[2], 'group_chat_id': row[3], 'bot_token': row[4], 'purchase_time': row[5]}
                for row in rows
            ]

    def check_user_purchased(self, user_id: int, product_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM purchases WHERE user_id = ? AND product_id = ?', (user_id, product_id))
            return c.fetchone() is not None 