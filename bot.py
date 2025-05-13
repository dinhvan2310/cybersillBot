import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import config
from handlers.command_handlers import start, menu_callback
from webhook_server import app as fastapi_app
import uvicorn

async def on_startup(app):
    print('cybersillBot is running!')

async def run_bot():
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(menu_callback))
    app.post_init = on_startup
    app.run_polling()

async def run_fastapi():
    config_uvicorn = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

async def main():
    await asyncio.gather(
        run_bot(),
        run_fastapi()
    )

if __name__ == '__main__':
    asyncio.run(main()) 