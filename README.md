## Chạy bot tự động với systemd

### 1. Tạo file service

Tạo file `/etc/systemd/system/cybersillbot.service` với nội dung (thay đổi thông tin cho phù hợp):

```ini
[Unit]
Description=Cybersill Bot Service
After=network.target

[Service]
Type=simple
User=youruser                # Thay bằng user chạy bot (không dùng root)
WorkingDirectory=/duong/dan/den/thu-muc-bot   # Đường dẫn tới thư mục bot
EnvironmentFile=/duong/dan/den/thu-muc-bot/.env  # Đường dẫn tới file .env
ExecStart=/usr/bin/node index.js              # Lệnh chạy bot (hoặc npm start)
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 2. Nạp lại systemd và bật service

```bash
sudo systemctl daemon-reload
sudo systemctl enable cybersillbot
sudo systemctl start cybersillbot
```

### 3. Tắt bot (dừng service)

```bash
sudo systemctl stop cybersillbot
```

### 4. Tắt hoàn toàn (không tự động khởi động lại khi reboot)

```bash
sudo systemctl disable cybersillbot
```

### 5. Kiểm tra trạng thái bot

```bash
sudo systemctl status cybersillbot
```

---

**Ghi chú:**  
- Sửa `youruser`, `WorkingDirectory`, `EnvironmentFile`, `ExecStart` cho đúng với môi trường của bạn.  
- File `.env` sẽ được systemd tự động nạp nếu bạn khai báo đúng đường dẫn với `EnvironmentFile`.
