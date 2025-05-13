import sqlite3

DB_PATH = 'test_db.sqlite3'

def create_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT
        )
    ''')
    print('Table created.')

def insert_user(conn, username, email):
    conn.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
    print(f'Inserted user: {username}')

def query_users(conn):
    cursor = conn.execute('SELECT id, username, email FROM users')
    print('All users:')
    for row in cursor:
        print(row)

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        create_table(conn)
        insert_user(conn, 'alice', 'alice@example.com')
        insert_user(conn, 'bob', 'bob@example.com')
        conn.commit()
        query_users(conn)
    finally:
        conn.close()
        print('Done.')

if __name__ == '__main__':
    main() 