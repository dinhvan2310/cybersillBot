import logging
import json
from datetime import datetime
from typing import Dict, Optional

from db.repositories.user_repository import UserRepository
from integrations.crypto_pay_api import CryptoPayAPI
from config import DEFAULT_MIN_DEPOSIT

logger = logging.getLogger(__name__)

class PaymentService:
    """Service for managing payments and user balance"""
    
    def __init__(self):
        self.crypto_pay = CryptoPayAPI()
    
    async def create_deposit_invoice(
        self,
        user_id: int,
        amount: float,
        asset: str = "USDT",
        description: str = None
    ) -> Dict:
        """
        Create a deposit invoice for a user
        
        Args:
            user_id: Telegram user ID
            amount: Amount to deposit
            asset: Cryptocurrency to use
            description: Invoice description
            
        Returns:
            Invoice data or error
        """
        if amount < DEFAULT_MIN_DEPOSIT:
            return {
                "ok": False,
                "error": f"Minimum deposit amount is {DEFAULT_MIN_DEPOSIT} {asset}"
            }
        
        # Ensure user exists
        user = await UserRepository.get_user_by_telegram_id(user_id)
        if not user:
            return {"ok": False, "error": "User not found"}
        
        # Create description if not provided
        if not description:
            description = f"Deposit {amount} {asset} to CyberSill Bot"
        
        # Create payload with user info for webhook handling
        payload = json.dumps({
            "user_id": user_id,
            "type": "deposit"
        })
        
        # Create invoice
        result = await self.crypto_pay.create_invoice(
            amount=amount,
            asset=asset,
            description=description,
            hidden_message=f"Thank you for your deposit of {amount} {asset}! Your balance has been updated.",
            payload=payload,
            allow_comments=True,
            allow_anonymous=False
        )
        
        if not result.get("ok", False):
            logger.error(f"Error creating invoice: {result.get('error')}")
            return result
        
        # Record pending invoice in database
        # This would typically store the invoice details in the payments table
        # For now, we'll just return the invoice data
        logger.info(f"Created deposit invoice for user {user_id}: {amount} {asset}")
        return result
    
    async def process_webhook_update(self, update_data: Dict) -> bool:
        """
        Process webhook update from Crypto Pay
        
        Args:
            update_data: Webhook data from Crypto Pay
            
        Returns:
            True if processed successfully, False otherwise
        """
        try:
            if update_data.get("update_type") != "invoice_paid":
                logger.warning(f"Unhandled update type: {update_data.get('update_type')}")
                return False
            
            invoice = update_data.get("payload", {})
            
            # Extract invoice data
            invoice_id = invoice.get("invoice_id")
            status = invoice.get("status")
            amount = float(invoice.get("amount", 0))
            asset = invoice.get("asset")
            
            # Skip if not paid
            if status != "paid":
                logger.info(f"Invoice {invoice_id} status is {status}, skipping")
                return False
            
            # Extract payload (contains user_id)
            try:
                payload = json.loads(invoice.get("payload", "{}"))
                user_id = payload.get("user_id")
                transaction_type = payload.get("type")
            except (json.JSONDecodeError, TypeError):
                logger.error(f"Invalid payload in invoice {invoice_id}")
                return False
            
            if not user_id or transaction_type != "deposit":
                logger.error(f"Missing user_id or type in payload for invoice {invoice_id}")
                return False
            
            # Update user balance
            success = await UserRepository.update_user_balance(user_id, amount, add=True)
            if not success:
                logger.error(f"Failed to update balance for user {user_id}")
                return False
            
            logger.info(f"Successfully processed deposit: {amount} {asset} for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}")
            return False
    
    async def get_user_balance(self, user_id: int) -> float:
        """Get user's current balance"""
        return await UserRepository.get_user_balance(user_id)
    
    async def deduct_balance(self, user_id: int, amount: float, description: str = None) -> bool:
        """
        Deduct amount from user balance
        
        Args:
            user_id: Telegram user ID
            amount: Amount to deduct
            description: Transaction description
            
        Returns:
            True if successful, False otherwise
        """
        # Check current balance
        current_balance = await self.get_user_balance(user_id)
        if current_balance < amount:
            logger.warning(f"Insufficient balance for user {user_id}: {current_balance} < {amount}")
            return False
        
        # Deduct from balance
        success = await UserRepository.update_user_balance(user_id, amount, add=False)
        if not success:
            logger.error(f"Failed to deduct balance for user {user_id}")
            return False
        
        logger.info(f"Deducted {amount} from user {user_id} balance")
        return True 