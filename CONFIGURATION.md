# HƯỚNG DẪN CẤU HÌNH DỰ ÁN cybersillBot

## 1. Yêu cầu hệ thống
- Python 3.9 trở lên
- pip (Python package manager)
- (Khuyến nghị) Git để clone project

## 2. Tải mã nguồn
Clone hoặc tải về mã nguồn dự án:
```bash
git clone <link-repo-của-bạn>
cd cybersillBot
```

## 3. Tạo và kích hoạt môi trường ảo
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

## 4. Cài đặt thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

## 5. Cấu hình biến môi trường
Tạo file `.env` ở thư mục gốc với nội dung:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
CRYPTO_PAY_API_TOKEN=your_crypto_pay_api_token
```
- `TELEGRAM_TOKEN`: Lấy từ [@BotFather](https://t.me/BotFather)
- `CRYPTO_PAY_API_TOKEN`: Lấy từ [@CryptoBot](https://t.me/CryptoBot) → Crypto Pay → My Apps

## 6. Thiết lập database
- Mặc định sử dụng SQLite, không cần cấu hình thêm.
- File database sẽ tự động tạo: `db.sqlite3`

## 7. Cấu hình ngôn ngữ
- Các file ngôn ngữ nằm trong thư mục `i18n/` (ví dụ: `en.json`, `vi.json`)
- Để thêm ngôn ngữ mới: copy file mẫu, dịch nội dung, lưu với mã ngôn ngữ tương ứng.

## 8. Cấu hình Crypto Pay Webhook
- Truy cập Crypto Pay Dashboard, bật webhook cho app của bạn.
- Nhập URL webhook: `https://<your-domain>/crypto-webhook`
- Nếu chạy local, dùng [ngrok](https://ngrok.com/) để tạo public URL:
  ```bash
  ngrok http 8000
  # Lấy link https://xxxx.ngrok.io/crypto-webhook để cấu hình webhook
  ```
- Đảm bảo cổng 8000 mở nếu deploy server thực tế.

## 9. Chạy bot và FastAPI server
```bash
python bot.py
```
- Bot Telegram và FastAPI sẽ chạy song song (xử lý webhook Crypto Pay)
- Mặc định FastAPI chạy ở `http://localhost:8000`

## 10. Lưu ý bảo mật
- Không commit file `.env` lên Git/public repo
- Không chia sẻ token bot, token Crypto Pay cho bất kỳ ai
- Nếu deploy thực tế, cấu hình HTTPS cho FastAPI (có thể dùng Nginx + Let's Encrypt hoặc uvicorn SSL trực tiếp)

## 11. Gợi ý triển khai thực tế
- Deploy trên VPS (Ubuntu), cài Python, cấu hình domain, SSL
- Sử dụng supervisor hoặc systemd để chạy bot và FastAPI như service
- Backup định kỳ file database `db.sqlite3`
- Theo dõi log để phát hiện lỗi sớm

## 12. Troubleshooting
- Nếu bot không phản hồi: kiểm tra token, kết nối mạng, log lỗi
- Nếu webhook không nhận: kiểm tra URL webhook, log FastAPI, cấu hình firewall
- Đọc log chi tiết trong terminal khi chạy bot

---
Mọi thắc mắc vui lòng liên hệ admin hoặc xem file hướng dẫn trong bot (nút "ℹ️ Hỗ trợ"). 