from fastapi import FastAPI, Request, Header, HTTPException
import hmac
import hashlib
import config

app = FastAPI()

@app.post("/crypto-webhook/{token}")
async def crypto_webhook(token: str, request: Request, crypto_pay_api_signature: str = Header(None)):
    body = await request.body()
    secret = hashlib.sha256(config.CRYPTO_PAY_API_KEY.encode()).digest()
    hmac_check = hmac.new(secret, body, hashlib.sha256).hexdigest()
    if crypto_pay_api_signature != hmac_check:
        raise HTTPException(status_code=403, detail="Invalid signature")
    data = await request.json()
    if data.get("update_type") == "invoice_paid":
        invoice = data["payload"]
        # TODO: Xử lý logic cập nhật DB, gửi file cho user, v.v.
        print("Invoice paid:", invoice)
    return {"ok": True}