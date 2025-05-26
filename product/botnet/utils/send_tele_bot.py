from telegram import Bot
from telegram import InputFile
from asyncio import sleep
from telegram.error import TimedOut

async def send_message(message, token, chat_id):
    try:
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
    except TimedOut as e:
        print(f"Error sending message: {e}")
    finally:
        await bot.close()

async def send_file(file_path, token, chat_id):
    bot = Bot(token=token)
    while True:
        try:
            with open(file_path, 'rb') as file:
                await bot.send_document(chat_id=chat_id, document=InputFile(file))
            return
        except TimedOut as e:
            print(f"Error sending file: {e}")
            await sleep(5)
            # Vòng lặp sẽ tự động thử lại, mở lại file mới
