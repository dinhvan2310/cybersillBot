# CyberSill Bot

A Telegram bot that manages user balances, allows users to purchase software/source code, and integrates with Crypto Pay API for adding funds.

## Features

- User registration and profile management
- Balance tracking and management
- Integration with Crypto Pay API for adding funds
- Software/source code catalog
- Purchase and delivery system

## Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/cybersillBot.git
cd cybersillBot
```

2. Create a virtual environment
```bash
python -m venv .venv
```

3. Activate the virtual environment
```bash
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your configuration
```
BOT_TOKEN=your_telegram_bot_token
CRYPTO_PAY_API_TOKEN=your_crypto_pay_api_token
DATABASE_URL=sqlite:///cybersill.db
ADMIN_USER_IDS=123456789,987654321
```

6. Run the bot
```bash
python bot.py
```

## Project Structure

- `bot.py` - Main bot entry point
- `config.py` - Configuration settings
- `handlers/` - Command and message handlers
- `models/` - Data models
- `services/` - Business logic
- `controllers/` - Bot interaction controllers
- `integrations/` - External API integrations
- `db/` - Database management 