# Tech Stack - cybersillBot

## Ngôn ngữ lập trình
- Python 3.x

## Framework & Thư viện chính
- python-telegram-bot: Xây dựng bot Telegram
- FastAPI: Xử lý webhook Crypto Pay
- aiosqlite: Tương tác SQLite bất đồng bộ
- python-dotenv: Quản lý biến môi trường
- requests/httpx: Giao tiếp HTTP
- markdown: Đọc file trợ giúp (hiện gửi plain text)

## Database
- SQLite

## Công cụ triển khai & phát triển
- Git: Quản lý mã nguồn
- VSCode/PyCharm: IDE phát triển
- (Tùy chọn) Docker: Đóng gói và triển khai

## Tích hợp khác
- Crypto Pay API: Thanh toán bằng tiền mã hóa (USDT)
- Telegram InlineKeyboard: Giao diện menu, chọn chức năng, chọn ngôn ngữ

## Kiến trúc
- Service/Repository pattern: Tách logic nghiệp vụ, thao tác DB, controller/handler
- Đa ngôn ngữ: Lưu trữ file JSON, hỗ trợ nhiều ngôn ngữ động 