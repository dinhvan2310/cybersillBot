import logging
from telegram.ext import Application

import config
from handlers.command_handlers import register_command_handlers
from db.database import init_database

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    import asyncio
    asyncio.run(init_database())
    logger.info("Database initialized")
    
    application = Application.builder().token(config.BOT_TOKEN).build()
    register_command_handlers(application)
    logger.info("Command handlers registered")
    
    application.run_polling()
    logger.info("Bot started successfully")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Error running bot: {e}") 