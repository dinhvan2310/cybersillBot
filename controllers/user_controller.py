from services.user_service import register_user

def handle_register_user(telegram_id, username, email=None, language="en"):
    user = register_user(telegram_id, username, email, language)
    return user 