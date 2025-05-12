import aiohttp
import logging
import hashlib
import hmac
import json
from typing import Dict, List, Optional, Union, Any
from datetime import datetime

from config import (
    CRYPTO_PAY_API_TOKEN,
    CRYPTO_PAY_API_BASE_URL,
    CRYPTO_PAY_WEBHOOK_SECRET,
    SUPPORTED_ASSETS,
)

logger = logging.getLogger(__name__)

class CryptoPayAPI:
    """Integration with Crypto Pay API for payments"""

    def __init__(self, api_token: str = None, base_url: str = None):
        self.api_token = api_token or CRYPTO_PAY_API_TOKEN
        self.base_url = base_url or CRYPTO_PAY_API_BASE_URL
        self.headers = {"Crypto-Pay-API-Token": self.api_token}

    async def _make_request(self, method: str, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Crypto Pay API"""
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            try:
                if method == "GET":
                    async with session.get(url, headers=self.headers, params=params) as response:
                        data = await response.json()
                else:  # POST
                    async with session.post(url, headers=self.headers, json=params) as response:
                        data = await response.json()
                
                if not data.get("ok", False):
                    logger.error(f"Crypto Pay API error: {data.get('error', 'Unknown error')}")
                    return {"ok": False, "error": data.get("error", "Unknown error")}
                
                return data
            except Exception as e:
                logger.error(f"Error making request to Crypto Pay API: {e}")
                return {"ok": False, "error": str(e)}

    async def get_me(self) -> Dict:
        """Test API token and get app info"""
        return await self._make_request("GET", "getMe")

    async def create_invoice(
        self,
        amount: float,
        asset: str = "USDT",
        description: str = None,
        hidden_message: str = None,
        paid_btn_name: str = None,
        paid_btn_url: str = None,
        payload: str = None,
        allow_comments: bool = True,
        allow_anonymous: bool = True,
        expires_in: int = 86400  # 24 hours
    ) -> Dict:
        """
        Create a new invoice for payment
        
        Args:
            amount: Amount to pay
            asset: Cryptocurrency code (USDT, TON, BTC, etc.)
            description: Invoice description
            hidden_message: Message shown after payment
            paid_btn_name: Button label after payment
            paid_btn_url: URL for button after payment
            payload: Additional data for this invoice
            allow_comments: Allow payment comments
            allow_anonymous: Allow anonymous payments
            expires_in: Time limit for payment in seconds
            
        Returns:
            Invoice data or error
        """
        if asset not in SUPPORTED_ASSETS:
            return {"ok": False, "error": f"Unsupported asset: {asset}"}
        
        params = {
            "asset": asset,
            "amount": str(amount),
            "description": description,
            "hidden_message": hidden_message,
            "paid_btn_name": paid_btn_name,
            "paid_btn_url": paid_btn_url,
            "payload": payload,
            "allow_comments": allow_comments,
            "allow_anonymous": allow_anonymous,
            "expires_in": expires_in
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return await self._make_request("POST", "createInvoice", params)

    async def get_invoices(
        self,
        asset: str = None,
        invoice_ids: List[str] = None,
        status: str = None,
        offset: int = 0,
        count: int = 100
    ) -> Dict:
        """Get invoices with optional filtering"""
        params = {
            "offset": offset,
            "count": count
        }
        
        if asset:
            params["asset"] = asset
        if invoice_ids:
            params["invoice_ids"] = ",".join(invoice_ids)
        if status:
            params["status"] = status
            
        return await self._make_request("GET", "getInvoices", params)

    async def get_balance(self) -> Dict:
        """Get current app balance"""
        return await self._make_request("GET", "getBalance")

    async def get_exchange_rates(self) -> Dict:
        """Get current exchange rates"""
        return await self._make_request("GET", "getExchangeRates")

    def verify_webhook_signature(self, request_data: str, signature: str) -> bool:
        """
        Verify webhook signature to ensure authenticity
        
        Args:
            request_data: Raw request body as string
            signature: Signature from request header
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not CRYPTO_PAY_WEBHOOK_SECRET:
            logger.warning("CRYPTO_PAY_WEBHOOK_SECRET not set, skipping signature verification")
            return True
            
        try:
            secret = hashlib.sha256(CRYPTO_PAY_API_TOKEN.encode()).digest()
            computed_signature = hmac.new(
                secret,
                msg=request_data.encode(),
                digestmod=hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(computed_signature, signature)
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False 