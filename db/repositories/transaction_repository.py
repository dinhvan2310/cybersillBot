import sqlite3
from models.transaction import Transaction
from datetime import datetime

class TransactionRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self.get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT,
                    description TEXT
                )
            ''')

    def add_transaction(self, user_id, type, amount, status, description=None):
        with self.get_conn() as conn:
            now = datetime.utcnow().isoformat()
            cur = conn.execute(
                'INSERT INTO transactions (user_id, type, amount, status, created_at, description) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, type, amount, status, now, description)
            )
            return cur.lastrowid

    def get_transactions_by_user(self, user_id):
        with self.get_conn() as conn:
            cur = conn.execute(
                'SELECT id, user_id, type, amount, status, created_at, description FROM transactions WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
            rows = cur.fetchall()
            return [Transaction(*row) for row in rows]

    def update_transaction_status(self, transaction_id, status):
        with self.get_conn() as conn:
            conn.execute(
                'UPDATE transactions SET status = ? WHERE id = ?',
                (status, transaction_id)
            ) 