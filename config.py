import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CRYPTO_PAY_API_TOKEN = os.getenv('CRYPTO_PAY_API_TOKEN')
DB_PATH = os.getenv('DB_PATH', 'db.sqlite3')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')