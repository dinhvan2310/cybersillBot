# cybersillBot

Telegram bot bán source code, tích hợp thanh toán Crypto Pay, quản lý user và gửi source code tự động.

## Mục tiêu
- Bán source code tự động qua Telegram
- Thanh toán nhanh chóng, bảo mật
- Quản lý user, giao dịch đơn giản

## Cài đặt nhanh
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

## Cấu trúc thư mục
- `bot.py`: Main bot entry
- `config.py`: Cấu hình
- `handlers/`: Command/message handlers
- `models/`, `services/`, `controllers/`: Logic chính
- `db/`: Database & repository
- `scripts/`: Script test
- `memory-bank/`: Lưu thông tin dự án 