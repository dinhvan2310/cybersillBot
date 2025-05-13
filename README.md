# cybersillBot

Bot Telegram bán source code tự động, tích hợp thanh toán Crypto Pay, quản lý người dùng và giao dịch, gửi file source code ngay trên Telegram.

## Mục tiêu
- Bán source code tự động qua Telegram
- Thanh toán nhanh, bảo mật bằng Crypto Pay
- Quản lý người dùng, giao dịch đơn giản

## Tính năng nổi bật
- **Đa ngôn ngữ:** Hỗ trợ Tiếng Việt, English, 中文, Русский, 日本語 (dễ mở rộng)
- **Đăng ký người dùng:** Tự động khi /start, chọn ngôn ngữ, quản lý số dư
- **Nạp tiền qua Crypto Pay:** Nạp USDT, nhận link thanh toán, tự động cộng số dư qua webhook
- **Mua source code:** Nếu đủ tiền, bot gửi file source code trực tiếp qua Telegram
- **Lịch sử giao dịch:** Xem lịch sử nạp tiền, mua code bằng ngôn ngữ đã chọn
- **Hỗ trợ/trợ giúp:** Xem file hướng dẫn đa ngôn ngữ ngay trên bot
- **Giao diện hiện đại:** Tất cả thao tác qua menu InlineKeyboard trên Telegram

## Hướng dẫn sử dụng

1. **Bắt đầu:**
   Gửi lệnh `/start` để đăng ký và truy cập menu chính
2. **Chọn ngôn ngữ:**
   Sử dụng menu chọn ngôn ngữ để đổi bất cứ lúc nào
3. **Nạp tiền:**
   Chọn "💸 Nạp tiền", nhập số USDT (tối thiểu 1), làm theo hướng dẫn thanh toán
4. **Mua code:**
   Chọn "🛒 Mua code". Nếu đủ tiền, bạn sẽ nhận file source code ngay
5. **Xem giao dịch:**
   Chọn "💳 Kiểm tra giao dịch" để xem lịch sử nạp/mua
6. **Trợ giúp:**
   Chọn "ℹ️ Hỗ trợ" để đọc hướng dẫn sử dụng bằng ngôn ngữ của bạn

## Cấu trúc dự án

```
cybersillBot/
  bot.py                  # Điểm khởi đầu bot
  config.py               # Cấu hình, biến môi trường
  handlers/               # Xử lý lệnh, callback, message Telegram
  controllers/            # Xử lý logic nghiệp vụ
  services/               # Service (user, payment, transaction, ngôn ngữ...)
  db/                     # Kết nối, repository thao tác dữ liệu
  models/                 # Định nghĩa model dữ liệu
  i18n/                   # File ngôn ngữ JSON, file trợ giúp markdown
  product/                # File source code bán cho user
  webhook_server.py       # FastAPI nhận webhook Crypto Pay
  requirements.txt        # Thư viện Python
  README.md               # Tài liệu dự án
  memory-bank/            # Tài liệu phân tích, kế hoạch, nghiệp vụ
```

## Mở rộng ngôn ngữ
- Thêm file JSON ngôn ngữ mới vào `i18n/` (ví dụ: `fr.json` cho tiếng Pháp)
- Thêm file trợ giúp markdown (ví dụ: `support_fr.md`)
- Cập nhật menu chọn ngôn ngữ trong `handlers/command_handlers.py` nếu cần

## Bảo trì & Bảo mật
- Dữ liệu user, giao dịch lưu bằng SQLite (dễ backup, di chuyển)
- Tích hợp Crypto Pay API bảo mật, xác thực webhook bằng HMAC-SHA256
- Kiến trúc service/repository rõ ràng, dễ mở rộng, bảo trì

## Hỗ trợ
- Sử dụng nút "ℹ️ Hỗ trợ" trên bot hoặc liên hệ admin (xem file trợ giúp)

## Tài liệu chi tiết [memory-bank](memory-bank)
- [project_info.md](memory-bank/project_info.md): Thông tin dự án
- [plan_detail.md](memory-bank/plan_detail.md): Kế hoạch phát triển
- [tech_stack.md](memory-bank/tech_stack.md): Công nghệ sử dụng
- [business_analysis.md](memory-bank/business_analysis.md): Phân tích nghiệp vụ

## Cài đặt nhanh
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Cấu hình
- Tạo file `.env` ở thư mục gốc:
```text
TELEGRAM_TOKEN =
CRYPTO_PAY_API_TOKEN =
```
- Cấu hình webhook trong dashboard Crypto Pay

## Chạy bot
```bash
python bot.py
```

## Tích hợp Crypto Pay API

- **Lấy API Token:**  
  Vào [@CryptoBot](https://t.me/CryptoBot) (hoặc [@CryptoTestnetBot](https://t.me/CryptoTestnetBot) cho testnet), vào **Crypto Pay → My Apps**, tạo app để lấy API Token.

- **Cấu hình webhook:**  
  - Trong app Crypto Pay, bật webhook và nhập URL FastAPI server (ví dụ: `https://yourdomain.com/crypto-webhook`)
  - Webhook gửi POST JSON tới endpoint của bạn (ví dụ: `https://yourdomain.com/crypto-webhook`)

Xem cập nhật mới nhất và tài liệu đầy đủ tại [Crypto Pay API Help Center](https://help.send.tg/en/articles/10279948-crypto-pay-api).
