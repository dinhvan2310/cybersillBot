# Thông tin dự án

## Tên dự án
cybersillBot

## Mô tả
Dự án cybersillBot là một Telegram bot bán source code. Sản phẩm chỉ là source code, không cần quản lý nhiều thông tin sản phẩm. Khi thanh toán thành công, bot sẽ gửi source code cho user.

## Cấu trúc dự án

### Core Bot Files
- `bot.py`: Điểm khởi đầu chính của bot
- `config.py`: Cài đặt cấu hình và biến môi trường
- `handlers/`: Thư mục chứa các handler cho lệnh và tin nhắn
  - `command_handlers.py`: Xử lý các lệnh bot
  - `callback_handlers.py`: Xử lý callback query
  - `message_handlers.py`: Xử lý tin nhắn văn bản

### User Management
- `models/user.py`: Mô hình dữ liệu người dùng
- `services/user_service.py`: Logic quản lý người dùng
- `controllers/user_controller.py`: Tương tác bot liên quan đến người dùng

### Payment System
- `services/payment_service.py`: Logic xử lý thanh toán
- `integrations/crypto_pay_api.py`: Tích hợp Crypto Pay API
- `models/transaction.py`: Mô hình dữ liệu giao dịch

### Product Management
- Sản phẩm: **Source code**
- Không cần quản lý nhiều thông tin sản phẩm
- Khi thanh toán thành công, bot gửi source code cho user
- `models/product.py`: Mô hình dữ liệu sản phẩm (đơn giản hóa)
- `services/product_service.py`: Logic gửi source code sau thanh toán
- `controllers/product_controller.py`: Tương tác bot liên quan đến việc gửi source code

### Database
- Sử dụng: **SQLite**
- `db/database.py`: Kết nối và thiết lập cơ sở dữ liệu
- `db/repositories/`: Lớp truy xuất dữ liệu
  - `user_repository.py`: Thao tác dữ liệu người dùng
  - `transaction_repository.py`: Thao tác dữ liệu giao dịch
  - `product_repository.py`: Thao tác dữ liệu sản phẩm

## Mục tiêu
- Xây dựng bot Telegram đa chức năng, dễ mở rộng
- Quản lý người dùng, sản phẩm, giao dịch hiệu quả
- Tích hợp thanh toán qua Crypto Pay
- Đảm bảo bảo mật và dễ bảo trì

## Ghi chú khác
- (Ghi chú bổ sung) 