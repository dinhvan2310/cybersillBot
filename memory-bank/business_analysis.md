# Phân tích nghiệp vụ dự án cybersillBot

## 0. Đa ngôn ngữ
- Bot hỗ trợ đa ngôn ngữ: Tiếng Việt, English, 中文, Русский, 日本語.
- Lưu ngôn ngữ ở file json, dễ dàng mở rộng/thay đổi.
- Tất cả tin nhắn, menu, giao dịch, trợ giúp... đều dùng đúng ngôn ngữ user chọn.

## 1. Đăng ký & quản lý người dùng
- Khi user nhấn /start, bot kiểm tra user đã tồn tại chưa.
- Nếu chưa có, bot đăng ký mới và lưu thông tin vào database (id, username, email, ngôn ngữ, balance).
- Nếu đã có, bot thông báo user đã đăng ký.
- User có thể đổi ngôn ngữ bất kỳ lúc nào qua menu.

## 2. Nạp tiền & Quản lý số dư
- User nạp tiền vào tài khoản qua Crypto Pay (USDT), bot tạo hóa đơn và gửi link thanh toán.
- Khi thanh toán thành công (qua webhook), số dư (balance) của user được cộng vào tài khoản.
- Số dư được lưu trong DB.
- User có thể kiểm tra số dư hiện tại qua menu.

## 3. Mua code (source code)
- User chọn chức năng "🛒 Mua code" trên bot.
- Bot kiểm tra số dư của user:
    - Nếu đủ tiền: trừ số dư, gửi source code cho user, thông báo thành công.
    - Nếu không đủ tiền: thông báo số dư không đủ, hướng dẫn nạp thêm tiền.
- Mỗi lần mua code đều tạo transaction (purchase).

## 4. Quản lý giao dịch
- Mỗi lần nạp tiền/mua code đều tạo transaction (deposit/purchase).
- User có thể kiểm tra lịch sử giao dịch (nạp tiền, mua code) qua menu.
- Lịch sử giao dịch hiển thị đúng ngôn ngữ user chọn.

## 5. Hỗ trợ & trợ giúp
- User có thể nhấn nút "ℹ️ Hỗ trợ" để nhận hướng dẫn sử dụng bot hoặc liên hệ admin.
- Hỗ trợ đa ngôn ngữ cho phần trợ giúp (file markdown, gửi plain text).

## 6. Giao diện người dùng
- Sử dụng InlineKeyboardButton và InlineKeyboardMarkup để tạo menu chức năng, chọn ngôn ngữ, nạp tiền, mua code, kiểm tra giao dịch, hỗ trợ...
- Giao diện tối ưu cho Telegram, dễ thao tác, đa ngôn ngữ.

## 7. Tích hợp & bảo mật
- Tích hợp Crypto Pay API cho thanh toán USDT.
- Xử lý webhook để cập nhật số dư tự động.
- Đảm bảo bảo mật, kiểm tra vận hành ổn định.

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