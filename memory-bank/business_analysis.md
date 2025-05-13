# Phân tích nghiệp vụ dự án cybersillBot

## 0. Đa ngôn ngữ
- Bot hỗ trợ đa ngôn ngữ: Tiếng Việt, English, ...
- Lưu ngôn ngữ ở file json sao cho dễ dàng sử dụng.

## 1. Đăng ký người dùng
- Khi user nhấn /start, bot kiểm tra user đã tồn tại chưa.
- Nếu chưa có, bot đăng ký mới và lưu thông tin vào database.
- Nếu đã có, bot thông báo user đã đăng ký.

## 2. Mua bot (source code)
- User chọn chức năng "🛒 Mua bot" trên bot hoặc gửi lệnh tương ứng.
- Bot hiển thị thông tin sản phẩm (bot/source code), giá và hướng dẫn thanh toán bằng ngôn ngữ user đã chọn.

## 3. Thanh toán qua Crypto Pay
- Bot tạo hóa đơn thanh toán qua Crypto Pay API.
- Gửi link thanh toán cho user.
- Theo dõi trạng thái hóa đơn (qua webhook hoặc polling).
- Thông báo trạng thái thanh toán bằng ngôn ngữ user đã chọn.

## 4. Gửi bot/source code cho user
- Khi nhận được xác nhận thanh toán thành công, bot tự động gửi file bot/source code cho user qua Telegram.
- Lưu lịch sử giao dịch vào database.
- Thông báo gửi file bằng ngôn ngữ phù hợp.

## 5. Kiểm tra giao dịch
- User có thể kiểm tra trạng thái giao dịch qua nút "💳 Kiểm tra giao dịch" hoặc lệnh tương ứng.
- Bot truy vấn trạng thái hóa đơn/giao dịch và trả kết quả cho user bằng ngôn ngữ đã chọn.

## 6. Hỗ trợ
- User có thể nhấn nút "ℹ️ Hỗ trợ" để nhận hướng dẫn sử dụng bot hoặc liên hệ admin.
- Hỗ trợ đa ngôn ngữ cho phần trợ giúp.

## Phụ lục: Cách triển khai menu dạng InlineKeyboard (Telegram)

- Sử dụng `InlineKeyboardButton` và `InlineKeyboardMarkup` để tạo menu dạng nút bấm trong tin nhắn.
- Mỗi nút có thể có `callback_data` (xử lý logic khi bấm) hoặc `url` (mở link ngoài).
- Ví dụ cấu hình menu:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Buy bot", callback_data='buy')],
    [
        InlineKeyboardButton("My profile", callback_data='profile'),
    ],
    [
        InlineKeyboardButton("Support ↗", url='https://t.me/support'),
    ],
    [InlineKeyboardButton("🇺🇸 >> 🇷🇺", callback_data='lang')]
]
reply_markup = InlineKeyboardMarkup(keyboard)
```

- Để xử lý sự kiện khi bấm nút, sử dụng `CallbackQueryHandler`:

```python
from telegram.ext import CallbackQueryHandler

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'buy':
        await query.edit_message_text("Bạn đã chọn mua subscription!")
    # Xử lý các callback_data khác tương tự
```

- Đăng ký handler:
```python
application.add_handler(CallbackQueryHandler(button_callback))
```

- Ưu điểm: giao diện đẹp, hiện đại, có thể mở link hoặc xử lý logic linh hoạt.
- Nhược điểm: không thay thế hoàn toàn bàn phím nhập liệu như ReplyKeyboardMarkup.