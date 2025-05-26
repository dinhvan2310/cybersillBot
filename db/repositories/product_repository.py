import sqlite3
from typing import Optional, List, Dict

class ProductRepository:
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    desc TEXT,
                    price REAL,
                    path TEXT
                )
            ''')
            conn.commit()

    def add_product(self, name: str, desc: str, price: float, path: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO products (name, desc, price, path) VALUES (?, ?, ?, ?)', (name, desc, price, path))
            conn.commit()
            return c.lastrowid

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, name, desc, price, path FROM products WHERE id = ?', (product_id,))
            row = c.fetchone()
            if row:
                return {'id': row[0], 'name': row[1], 'desc': row[2], 'price': row[3], 'path': row[4]}
            return None

    def get_all_products(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, name, desc, price, path FROM products')
            rows = c.fetchall()
            return [
                {'id': row[0], 'name': row[1], 'desc': row[2], 'price': row[3], 'path': row[4]}
                for row in rows
            ]

    def update_product(self, product_id: int, name: str, desc: str, price: float, path: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE products SET name = ?, desc = ?, price = ?, path = ? WHERE id = ?
            ''', (name, desc, price, path, product_id))
            conn.commit()
            return c.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            return c.rowcount > 0 