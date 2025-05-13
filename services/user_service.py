from db.repositories.user_repository import UserRepository
import config

user_repo = UserRepository(config.DB_PATH)

def register_user(telegram_id, username, email=None, language="en"):
    user_repo.add_user(telegram_id, username, email, language)
    return user_repo.get_user_by_telegram_id(telegram_id)

def get_user(telegram_id):
    return user_repo.get_user_by_telegram_id(telegram_id)

def update_user_language(telegram_id, language):
    user_repo.update_user_language(telegram_id, language)
    return user_repo.get_user_by_telegram_id(telegram_id)
