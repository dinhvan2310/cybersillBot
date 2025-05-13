from db.repositories.user_repository import UserRepository
import config

def init_db():
    user_repo = UserRepository(config.DB_PATH)
    user_repo.create_table()

if __name__ == '__main__':
    init_db()
    print('Database initialized!') 