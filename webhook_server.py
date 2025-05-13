from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import config
from services.user_service import get_user_by_telegram_id, update_user_balance
from services.transaction_service import update_transaction_status

app = FastAPI()

@app.post("/crypto-webhook")
async def crypto_webhook(request: Request, crypto_pay_api_signature: str = Header(None)):
    body = await request.body()
    secret = hashlib.sha256(config.CRYPTO_PAY_API_KEY.encode()).digest()
    hmac_check = hmac.new(secret, body, hashlib.sha256).hexdigest()
    if crypto_pay_api_signature != hmac_check:
        raise HTTPException(status_code=403, detail="Invalid signature")
    data = await request.json()
    if data.get("update_type") == "invoice_paid":
        invoice = data["payload"]
        user_id = invoice.get("user_id")
        amount = float(invoice.get("amount", 0))
        if user_id and amount > 0:
            user = get_user_by_telegram_id(user_id)
            if user:
                new_balance = (user.balance or 0) + amount
                update_user_balance(user_id, new_balance)
                print(f"Cộng {amount} USDT cho user {user_id}. Số dư mới: {new_balance}")
        print("Invoice paid:", invoice)
    return {"ok": True}