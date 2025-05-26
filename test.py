from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
import time
import re

# Thiết lập Telethon Client
api_id = 10016773 # Thay bằng API ID của bạn
api_hash = '788b3df4ef36b07ee6c8f75099b08bb2'  # Thay bằng API Hash của bạn
phone = '+84708137908'  # Thay bằng số điện thoại của bạn

client = TelegramClient('session_name', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# Tạo supergroup
channel = client(CreateChannelRequest(
    title="My New Groupp2",
    about="Description",
    megagroup=True
))
chat_id = channel.chats[0].id
print(f"Created group with chat_id: {chat_id}")

# Tạo bot mới
botfather = client.get_entity('BotFather')

# Gửi /newbot
client.send_message(botfather, '/newbot')
time.sleep(1)

# Gửi tên cho bot
client.send_message(botfather, 'MyTestBot')
time.sleep(1)

# Gửi username cho bot
client.send_message(botfather, '@nezukosuzumeeee_bot')
time.sleep(1)

# Lấy tin nhắn cuối cùng từ BotFather chứa token
messages = client.get_messages(botfather, limit=1)
last_message = messages[0]
print(last_message.text)

# Phân tích token
token_match = re.search(r"(\d+:\w+)", last_message.text)
if token_match:
    bot_token = token_match.group(1)
    print(f"Bot token: {bot_token}")
else:
    print("Could not find token")
    exit()

# Lấy entity của bot bằng username
bot_username = '@nezukosuzumeeee_bot'
bot_entity = client.get_entity(bot_username)
print(f"Bot entity: {bot_entity.id}")

# Thêm bot vào nhóm
client(InviteToChannelRequest(
    channel=channel.chats[0],
    users=[bot_entity]
))
print("Bot added to group")

# Thêm người dùng bất kỳ vào nhóm (ví dụ: username 'someuser')
try:
    user_to_add_username = '@dinhvan0294'
    user_to_add = client.get_entity(user_to_add_username)
    client(InviteToChannelRequest(
        channel=channel.chats[0],
        users=[user_to_add]
    ))
    print(f"Added {user_to_add_username} to the group")
except Exception as e:
    print(f"Error adding user: {e}")

# Trả về token và chat ID
print(f"Bot token: {bot_token}")
print(f"Group chat ID: {chat_id}")