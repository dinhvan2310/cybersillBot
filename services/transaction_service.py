from db.repositories.transaction_repository import TransactionRepository
import config

transaction_repo = TransactionRepository(config.DB_PATH)

def add_transaction(user_id, type, amount, status, description=None):
    return transaction_repo.add_transaction(user_id, type, amount, status, description)

def get_transactions_by_user(user_id):
    return transaction_repo.get_transactions_by_user(user_id)

def update_transaction_status(transaction_id, status):
    return transaction_repo.update_transaction_status(transaction_id, status) 