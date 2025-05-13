import sqlite3
from models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self.get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    email TEXT,
                    created_at TEXT
                )
            ''')

    def add_user(self, telegram_id, username, email=None, language="en"):
        with self.get_conn() as conn:
            now = datetime.utcnow().isoformat()
            conn.execute(
                'INSERT OR IGNORE INTO users (telegram_id, username, email, language, created_at) VALUES (?, ?, ?, ?, ?)',
                (telegram_id, username, email, language, now)
            )

    def get_user_by_telegram_id(self, telegram_id):
        with self.get_conn() as conn:
            cur = conn.execute('SELECT id, telegram_id, username, email, language, created_at FROM users WHERE telegram_id = ?', (telegram_id,))
            row = cur.fetchone()
            if row:
                return User(*row)
            return None

    def update_user_language(self, telegram_id, language):
        with self.get_conn() as conn:
            conn.execute(
                'UPDATE users SET language = ? WHERE telegram_id = ?',
                (language, telegram_id)
            ) 