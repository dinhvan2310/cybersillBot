import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

# Crypto Pay API Configuration
CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN")
CRYPTO_PAY_WEBHOOK_URL = os.getenv("CRYPTO_PAY_WEBHOOK_URL")
CRYPTO_PAY_WEBHOOK_SECRET = os.getenv("CRYPTO_PAY_WEBHOOK_SECRET")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cybersill.db")

# Admin User IDs
ADMIN_USER_IDS = [int(user_id) for user_id in os.getenv("ADMIN_USER_IDS", "").split(",") if user_id]

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if DEBUG else logging.INFO,
)
logger = logging.getLogger(__name__)

# Crypto Pay API URLs
CRYPTO_PAY_API_BASE_URL = "https://pay.crypt.bot/api"
if DEBUG:
    CRYPTO_PAY_API_BASE_URL = "https://testnet-pay.crypt.bot/api"

# Supported cryptocurrencies
SUPPORTED_ASSETS = ["USDT", "TON", "BTC", "ETH", "LTC", "BNB", "TRX", "USDC"]

# Default minimum deposit amount
DEFAULT_MIN_DEPOSIT = 1.0 