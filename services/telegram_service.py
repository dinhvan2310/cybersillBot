from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
import requests
import config

class TelegramService:
    def __init__(self, api_id = config.API_ID, api_hash = config.API_HASH, phone = config.PHONE, session_name='session_name'):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_name = session_name
        self.client = TelegramClient(session_name, api_id, api_hash)

    async def start(self):
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            code = input('Enter the code: ')
            await self.client.sign_in(self.phone, code)

    async def create_group(self, title, about):
        channel = await self.client(CreateChannelRequest(
            title=title,
            about=about,
            megagroup=True
        ))
        return channel.chats[0]

    async def add_bot_to_group(self, bot_username, group):
        bot_entity = await self.client.get_entity(bot_username)
        await self.client(InviteToChannelRequest(
            channel=group,
            users=[bot_entity]
        ))
        return True

    async def add_user_to_group(self, user_username, group):
        user_entity = await self.client.get_entity(user_username)
        await self.client(InviteToChannelRequest(
            channel=group,
            users=[user_entity]
        ))
        return True

    async def setup_group_with_bot(self, group_title, group_about, user_to_add=None, bot_token=None, bot_username=None):
        await self.start()
        group = await self.create_group(group_title, group_about)
        await self.add_bot_to_group(bot_username, group)
        
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates')
        data = response.json()
        chat_id = None
        for item in data['result']:
            message = item.get('message')
            if not message or message.get('chat') is None:
                continue
            if message['chat']['title'] == group_title:
                chat_id = message['chat']['id']
                break
        print(chat_id)
        if user_to_add:
            await self.add_user_to_group(user_to_add, group)
        return {
            'bot_token': bot_token,
            'bot_username': bot_username,
            'group_chat_id': chat_id,
        } 
        
    async def send_file(self, file_path, token, chat_id):
        await self.client.start(bot_token=token)
        await self.client.send_file(chat_id, file_path)
    
    async def send_message(self, message, token, chat_id):
        await self.client.start(bot_token=token)
        await self.client.send_message(chat_id, message)