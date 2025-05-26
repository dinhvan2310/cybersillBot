import sys
from telegram import Bot
import asyncio

async def test_bot_token(bot_token, chat_id):
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text="✅ Bot token và chat_id hợp lệ! Bot đã gửi được tin nhắn.")
        print("Gửi tin nhắn thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    bot_token = '7651687881:AAGa8_Z245oMqx97dv5ijlWwGh1XwiibbmI'
    chat_id = '-1002694612207'
    asyncio.run(test_bot_token(bot_token, chat_id)) 