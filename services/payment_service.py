import requests
import config

API_URL = "https://pay.crypt.bot/api/"
CRYPTO_PAY_API_TOKEN = config.CRYPTO_PAY_API_TOKEN

def get_me():
    url = API_URL + "getMe"
    headers = {"Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN}
    return requests.get(url, headers=headers).json()

def create_invoice(asset, amount, description, hidden_message=None):
    url = API_URL + "createInvoice"
    headers = {"Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN}
    data = {
        "asset": asset,  # e.g. "USDT"
        "amount": str(amount),
        "description": description,
    }
    if hidden_message:
        data["hidden_message"] = hidden_message
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_invoice(invoice_id):
    url = API_URL + "getInvoices"
    headers = {"Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN}
    params = {"invoice_ids": invoice_id}
    response = requests.get(url, headers=headers, params=params)
    return response.json() 