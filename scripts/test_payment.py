from services.payment_service import get_me, create_invoice, get_invoice

print("Test get_me:", get_me())

invoice = create_invoice("USDT", 2, "Test thanh toán", "Cảm ơn bạn!")
print("Tạo hóa đơn:", invoice)

if invoice.get("ok"):
    invoice_id = invoice["result"]["invoice_id"]
    print("Kiểm tra hóa đơn:", get_invoice(invoice_id))