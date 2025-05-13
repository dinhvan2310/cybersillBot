import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_PAY_API_TOKEN = os.getenv('CRYPTO_PAY_API_TOKEN')
DB_PATH = os.getenv('DB_PATH', 'db.sqlite3')
PRICE_PER_CODE = 5.0 