from db.repositories.user_repository import UserRepository, get_user_by_telegram_id as repo_get_user_by_telegram_id
import config

user_repo = UserRepository(config.DB_PATH)

def register_user(telegram_id, username, email=None, language="en", balance=0.0):
    user_repo.add_user(telegram_id, username, email, language, balance)
    return user_repo.get_user_by_telegram_id(telegram_id)

def get_user(telegram_id):
    return user_repo.get_user_by_telegram_id(telegram_id)

def update_user_language(telegram_id, language):
    user_repo.update_user_language(telegram_id, language)
    return user_repo.get_user_by_telegram_id(telegram_id)

def get_user_by_telegram_id(telegram_id):
    return repo_get_user_by_telegram_id(telegram_id)

def update_user_balance(telegram_id, balance):
    user_repo.update_user_balance(telegram_id, balance)
    return user_repo.get_user_by_telegram_id(telegram_id)
