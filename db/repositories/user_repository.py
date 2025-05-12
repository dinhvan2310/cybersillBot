import logging
import aiosqlite
from datetime import datetime
from db.database import get_connection

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for user-related database operations"""

    @staticmethod
    async def create_user(telegram_id, username=None, first_name=None, last_name=None):
        """Create a new user entry"""
        async with await get_connection() as db:
            try:
                query = """
                INSERT INTO users (telegram_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
                """
                await db.execute(query, (telegram_id, username, first_name, last_name))
                await db.commit()
                logger.info(f"User created with telegram_id: {telegram_id}")
                return await UserRepository.get_user_by_telegram_id(telegram_id)
            except aiosqlite.IntegrityError:
                logger.warning(f"User with telegram_id: {telegram_id} already exists")
                return await UserRepository.get_user_by_telegram_id(telegram_id)
            except Exception as e:
                logger.error(f"Error creating user: {e}")
                raise

    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        """Get user by telegram_id"""
        async with await get_connection() as db:
            db.row_factory = aiosqlite.Row
            query = "SELECT * FROM users WHERE telegram_id = ?"
            cursor = await db.execute(query, (telegram_id,))
            user = await cursor.fetchone()
            return dict(user) if user else None

    @staticmethod
    async def update_user_balance(telegram_id, amount, add=True):
        """Update user balance by adding or subtracting"""
        async with await get_connection() as db:
            try:
                query = """
                UPDATE users 
                SET balance = balance + ?, 
                    last_active = ?
                WHERE telegram_id = ?
                """
                if not add:
                    amount = -abs(amount)  # Ensure amount is negative if subtracting
                
                current_time = datetime.now().isoformat()
                await db.execute(query, (amount, current_time, telegram_id))
                await db.commit()
                logger.info(f"Updated balance for user {telegram_id}: {'added' if add else 'subtracted'} {abs(amount)}")
                return True
            except Exception as e:
                logger.error(f"Error updating user balance: {e}")
                return False

    @staticmethod
    async def get_user_balance(telegram_id):
        """Get user's current balance"""
        user = await UserRepository.get_user_by_telegram_id(telegram_id)
        return user['balance'] if user else 0.0

    @staticmethod
    async def update_last_active(telegram_id):
        """Update user's last active timestamp"""
        async with await get_connection() as db:
            try:
                query = "UPDATE users SET last_active = ? WHERE telegram_id = ?"
                current_time = datetime.now().isoformat()
                await db.execute(query, (current_time, telegram_id))
                await db.commit()
                return True
            except Exception as e:
                logger.error(f"Error updating last active: {e}")
                return False

    @staticmethod
    async def is_admin(telegram_id):
        """Check if user is an admin"""
        user = await UserRepository.get_user_by_telegram_id(telegram_id)
        return bool(user and user['is_admin']) 