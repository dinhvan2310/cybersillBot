# Thông tin dự án

## Tên dự án
cybersillBot

## Mô tả
cybersillBot là một Telegram bot bán source code tự động, hỗ trợ đa ngôn ngữ, thanh toán qua Crypto Pay (USDT), quản lý số dư, giao dịch, và gửi file source code cho user sau khi thanh toán thành công. Toàn bộ trải nghiệm được tối ưu cho Telegram, dễ thao tác, đa ngôn ngữ, và bảo mật.

## Tính năng chính
- Đăng ký & quản lý người dùng (ngôn ngữ, balance, username...)
- Đa ngôn ngữ: Tiếng Việt, English, 中文, Русский, 日本語 (dễ mở rộng)
- Nạp tiền qua Crypto Pay API (USDT), xử lý webhook tự động cộng số dư
- Mua code: kiểm tra số dư, trừ tiền, gửi file source code qua Telegram
- Quản lý giao dịch: lưu lịch sử nạp tiền/mua code, hiển thị đa ngôn ngữ
- Hỗ trợ/trợ giúp: gửi file hướng dẫn sử dụng bot (đa ngôn ngữ, plain text)
- Giao diện menu, chọn chức năng, chọn ngôn ngữ bằng InlineKeyboard
- Kiến trúc service/repository rõ ràng, dễ bảo trì, mở rộng

## Cấu trúc dự án (thực tế)
- `bot.py`: Điểm khởi đầu chính của bot
- `config.py`: Cài đặt cấu hình và biến môi trường
- `handlers/`: Chứa các handler cho lệnh, callback, message
  - `command_handlers.py`: Xử lý menu, giao dịch, trợ giúp, nạp tiền, mua code...
- `controllers/`: Controller logic cho user, product, transaction...
- `services/`: Xử lý nghiệp vụ (user, payment, transaction, ngôn ngữ...)
- `db/`: Kết nối, repository thao tác dữ liệu (user, transaction...)
- `models/`: Định nghĩa model dữ liệu
- `i18n/`: File ngôn ngữ JSON, file trợ giúp markdown đa ngôn ngữ
- `product/`: Chứa file source code bán cho user
- `webhook_server.py`: FastAPI nhận webhook từ Crypto Pay

## Mục tiêu
- Xây dựng bot Telegram đa chức năng, dễ mở rộng, bảo trì
- Quản lý người dùng, giao dịch, sản phẩm hiệu quả
- Tích hợp thanh toán Crypto Pay, tự động hóa toàn bộ quy trình
- Đảm bảo bảo mật, trải nghiệm người dùng tốt nhất

## Điểm nổi bật
- Đa ngôn ngữ toàn diện, dễ mở rộng
- Tích hợp Crypto Pay, tự động cộng số dư qua webhook
- Transaction rõ ràng, minh bạch
- Hỗ trợ/trợ giúp đa ngôn ngữ, gửi plain text
- UI Telegram hiện đại, dễ thao tác
- Kiến trúc service/repository, dễ bảo trì

## Ghi chú khác
- (Ghi chú bổ sung) 