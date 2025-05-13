import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
import config
from handlers.command_handlers import start, menu_callback, deposit_start, deposit_amount, DEPOSIT_AMOUNT
from webhook_server import app as fastapi_app
import uvicorn


async def run_bot():
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    # Handler cho các callback query khác ngoài deposit
    app.add_handler(CallbackQueryHandler(menu_callback, pattern="^(?!deposit$).*"))

    # ConversationHandler chỉ cho flow deposit
    deposit_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(deposit_start, pattern="^deposit$")],
        states={
            DEPOSIT_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount)],
        },
        fallbacks=[],
    )
    app.add_handler(deposit_conv)

    await app.initialize()
    await app.start()
    print('cybersillBot is running!')
    await app.updater.start_polling()
    try:
        while True:
            await asyncio.sleep(3600)
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Shutting down bot...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

async def run_fastapi():
    config_uvicorn = uvicorn.Config(
        fastapi_app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()

async def main():
    bot_task = asyncio.create_task(run_bot())
    fastapi_task = asyncio.create_task(run_fastapi())
    await asyncio.gather(bot_task, fastapi_task)

if __name__ == '__main__':
    asyncio.run(main()) 