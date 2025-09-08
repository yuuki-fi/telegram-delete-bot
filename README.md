# Telegram Delete Bot

Bot Telegram tự động xoá tin nhắn chứa link `https://t.me/` hoặc `t.me/`.

## Các lệnh quản trị
- `/addblock <link>` → Thêm link vào blocklist
- `/removeblock <link>` → Xoá link khỏi blocklist
- `/listblock` → Xem danh sách link đang bị chặn

⚠️ Chỉ admin nhóm mới có thể dùng các lệnh này.

## Deploy trên Render
1. Upload repo này lên GitHub.
2. Vào [Render](https://render.com/) → New Web Service.
3. Kết nối GitHub repo.
4. Environment Variables:
   - `BOT_TOKEN=YOUR_BOT_TOKEN`
5. Build Command:
   ```
   pip install -r requirements.txt
   ```
6. Start Command:
   ```
   python bot.py
   ```
