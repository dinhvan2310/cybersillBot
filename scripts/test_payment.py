from services.payment_service import create_invoice, get_invoice
import time

# 1. Tạo hóa đơn mới
result = create_invoice(
    asset="USDT",  # hoặc "TON", "BTC", ...
    amount=1.5,    # Số tiền muốn test
    description="Thanh toán test bot/source code",
    hidden_message="Cảm ơn bạn đã thanh toán!"
)
print("Kết quả tạo hóa đơn:", result)

if not result.get("ok"):
    print("Tạo hóa đơn thất bại:", result.get("error"))
    exit(1)

invoice = result["result"]
invoice_id = invoice["invoice_id"]
invoice_url = invoice["bot_invoice_url"]

print(f"\nLink thanh toán (gửi cho user hoặc tự mở Telegram):\n{invoice_url}")
print(f"Invoice ID: {invoice_id}")

# 2. Chờ user thanh toán, kiểm tra trạng thái hóa đơn
print("\nChờ thanh toán... (bạn có thể mở link trên Telegram và thanh toán thử)")
for i in range(10):
    time.sleep(10)  # Chờ 10 giây mỗi lần kiểm tra
    status = get_invoice(invoice_id)
    print(f"Lần kiểm tra {i+1}: {status}")
    if status.get("ok"):
        invoice_status = status["result"]["invoices"][0]["status"]
        print(f"Trạng thái hóa đơn: {invoice_status}")
        if invoice_status == "paid":
            print("Đã thanh toán thành công!")
            break
    else:
        print("Lỗi khi kiểm tra hóa đơn:", status.get("error"))