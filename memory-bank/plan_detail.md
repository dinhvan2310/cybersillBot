# Kế hoạch phát triển dự án cybersillBot

## 🗣️ Đa ngôn ngữ
- [x] Thiết kế cấu trúc lưu trữ ngôn ngữ (file JSON)
- [x] Xây dựng module load/chọn/sử dụng ngôn ngữ động
- [x] Tích hợp đa ngôn ngữ vào các chức năng bot (menu, giao dịch, trợ giúp...)

## 👤 Quản lý người dùng
- [x] Thiết kế model user (có trường ngôn ngữ, balance)
- [x] Repository thao tác DB user (CRUD, lưu ngôn ngữ, balance)
- [x] Service/controller/handler đăng ký & kiểm tra user
- [x] Đổi ngôn ngữ động qua menu

## 💰 Nạp tiền & Quản lý số dư
- [x] Tích hợp Crypto Pay API cho nạp tiền (USDT)
    - [x] Tìm hiểu tài liệu, tạo module/service tích hợp API
    - [x] Hàm tạo hóa đơn nạp tiền, kiểm tra hóa đơn, xử lý webhook
- [x] Gửi link nạp tiền cho user
    - [x] Tạo hóa đơn khi user chọn nạp tiền
    - [x] Gửi link nạp tiền, hướng dẫn user (đa ngôn ngữ)
- [x] Cộng số dư cho user khi thanh toán thành công (qua webhook)
    - [x] Xử lý webhook: cộng balance cho user
- [x] Cho phép user kiểm tra số dư hiện tại

## 📊 Tra cứu giao dịch
- [x] Tạo model giao dịch
- [x] Repository thao tác DB giao dịch (CRUD)
- [x] Service/controller/handler tra cứu giao dịch
- [x] Lưu lịch sử nạp tiền/mua code (transaction)
- [x] Hiển thị lịch sử giao dịch đa ngôn ngữ

## 🤖 Mua bot (source code)
- [x] Hard code thông tin sản phẩm (bot/source code) trong code hoặc file cấu hình
- [x] Khi user chọn mua bot:
    - [x] Kiểm tra balance
    - [x] Nếu đủ tiền: trừ balance, gửi file cho user
    - [x] Nếu không đủ: thông báo số dư không đủ, hướng dẫn nạp thêm

## 🆘 Hỗ trợ & trợ giúp
- [x] Handler/giao diện trợ giúp, hướng dẫn sử dụng bot
- [x] Hỗ trợ đa ngôn ngữ cho phần trợ giúp (file markdown, gửi dạng plain text)

## 🖼️ UI/Giao diện người dùng
- [x] Giao diện chọn chức năng chính (menu), command /start
- [x] Giao diện nạp tiền
- [x] Giao diện mua bot/source code
- [x] Giao diện kiểm tra số dư/giao dịch
- [x] Giao diện trợ giúp/hỗ trợ
- [x] Giao diện chọn ngôn ngữ
- [x] Tối ưu trải nghiệm người dùng, đảm bảo dễ thao tác trên Telegram (ReplyKeyboard, InlineKeyboard)

## 🛠️ Khác
- [x] Kiểm tra bảo mật, vận hành ổn định
- [x] Đóng gói, triển khai bot lên server/cloud 