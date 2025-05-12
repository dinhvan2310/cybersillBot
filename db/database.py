import os
import aiosqlite
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Database file path
DB_PATH = Path("cybersill.db")

# SQL scripts for table creation
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    balance REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin INTEGER DEFAULT 0
);
"""

CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category_id INTEGER,
    file_path TEXT,
    preview_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
"""

CREATE_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);
"""

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (payment_id) REFERENCES payments (id)
);
"""

CREATE_PURCHASES_TABLE = """
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    transaction_id INTEGER NOT NULL,
    purchase_price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_status TEXT DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (transaction_id) REFERENCES transactions (id)
);
"""

CREATE_PAYMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    invoice_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL,
    amount REAL NOT NULL,
    asset TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP,
    transaction_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (transaction_id) REFERENCES transactions (id)
);
"""

async def get_connection():
    """Get SQLite connection"""
    return await aiosqlite.connect(DB_PATH)

async def init_database():
    """Initialize the database tables"""
    logger.info("Initializing database...")
    async with await get_connection() as db:
        # Create tables in the correct order to maintain foreign key constraints
        await db.execute(CREATE_USERS_TABLE)
        await db.execute(CREATE_CATEGORIES_TABLE)
        await db.execute(CREATE_PRODUCTS_TABLE)
        await db.execute(CREATE_PAYMENTS_TABLE)
        await db.execute(CREATE_TRANSACTIONS_TABLE)
        await db.execute(CREATE_PURCHASES_TABLE)
        await db.commit()
        logger.info("Database initialized successfully.")

async def close_database(db):
    """Close database connection"""
    if db:
        await db.close()
        logger.info("Database connection closed.") 