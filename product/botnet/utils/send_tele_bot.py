import requests
from asyncio import sleep

# https://{YOUR_WORKER_URL}/bot{YOUR_BOT_TOKEN}/sendMessage
YOUR_WORKER_URL = 'plantsnap.trandinhvan0294.workers.dev'
async def send_message(message, token, chat_id):
    url = f"https://{YOUR_WORKER_URL}/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Error sending message: {response.text}")

async def send_file(file_path, token, chat_id):
    url = f"https://{YOUR_WORKER_URL}/bot{token}/sendDocument"
    while True:
        try:
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {'chat_id': chat_id}
                response = requests.post(url, files=files, data=data, timeout=10)
                if response.status_code == 200:
                    print("File sent successfully")
                    return
                else:
                    print(f"Error sending file: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending file: {e}")
            await sleep(5)
            # Vòng lặp sẽ tự động thử lại
