import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ Lấy token từ biến môi trường
TOKEN = os.getenv("BOT_TOKEN")

# File lưu danh sách blocklist
BLOCKLIST_FILE = "blocklist.json"

# Tải blocklist từ file (nếu có)
if os.path.exists(BLOCKLIST_FILE):
    with open(BLOCKLIST_FILE, "r", encoding="utf-8") as f:
        BLOCKED_PREFIXES = json.load(f)
else:
    BLOCKED_PREFIXES = ["https://t.me/", "t.me/"]

def save_blocklist():
    with open(BLOCKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(BLOCKED_PREFIXES, f, ensure_ascii=False, indent=2)

# 🛑 Xoá tin nhắn spam
async def delete_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text:
        for prefix in BLOCKED_PREFIXES:
            if text.startswith(prefix):
                try:
                    await update.message.delete()
                    print(f"🚫 Đã xoá tin nhắn: {text}")
                except Exception as e:
                    print(f"Lỗi khi xoá: {e}")
                break

# 🔐 Check quyền admin
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

# ➕ Thêm link
async def add_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    if not context.args:
        await update.message.reply_text("❌ Dùng: /addblock <link>")
        return

    prefix = context.args[0]
    if prefix not in BLOCKED_PREFIXES:
        BLOCKED_PREFIXES.append(prefix)
        save_blocklist()
        await update.message.reply_text(f"✅ Đã thêm vào blocklist: {prefix}")
    else:
        await update.message.reply_text("ℹ️ Link đã có trong blocklist.")

# ➖ Xoá link
async def remove_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    if not context.args:
        await update.message.reply_text("❌ Dùng: /removeblock <link>")
        return

    prefix = context.args[0]
    if prefix in BLOCKED_PREFIXES:
        BLOCKED_PREFIXES.remove(prefix)
        save_blocklist()
        await update.message.reply_text(f"✅ Đã xoá khỏi blocklist: {prefix}")
    else:
        await update.message.reply_text("ℹ️ Link không có trong blocklist.")

# 📋 Xem blocklist
async def list_block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Bạn không có quyền dùng lệnh này.")
        return

    if BLOCKED_PREFIXES:
        text = "📜 Danh sách blocklist:\n" + "\n".join(f"- {p}" for p in BLOCKED_PREFIXES)
    else:
        text = "✅ Blocklist đang trống."
    await update.message.reply_text(text)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN chưa được cung cấp. Hãy thêm Environment Variable trên Render.")

    app = ApplicationBuilder().token(TOKEN).build()

    # Lắng nghe tin nhắn văn bản
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_spam))

    # Lệnh quản trị
    app.add_handler(CommandHandler("addblock", add_block))
    app.add_handler(CommandHandler("removeblock", remove_block))
    app.add_handler(CommandHandler("listblock", list_block))

    print("✅ Bot đang chạy với quyền admin kiểm soát...")
    app.run_polling()
