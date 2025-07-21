from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import threading
from flask import Flask

# ✅ Web server for uptime (Render ping)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def start_server():
    thread = threading.Thread(target=run)
    thread.start()

start_server()

# ✅ Bot Token & Constants
BOT_TOKEN = "7588601306:AAHovG-BWMOm3rs9k94rMDmPrTpREIBY-R8"
ADMIN_ID = 7881285373
GROUP_LINK = "https://t.me/+HGrIvWqrAkw1OGU1"
UPI_ID = "squad.support@ibl"

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 नमस्ते {user.first_name}!\n\n"
        "👉 Squad Group YT जॉइन करने के लिए ₹100 का पेमेंट करना होगा।\n\n"
        f"💸 *UPI ID:* `{UPI_ID}`\n"
        "🧾 कृपया पेमेंट करने के बाद Screenshot भेजें।\n\n"
        "👇 QR Code यहाँ है:",
        parse_mode="Markdown"
    )

    qr_path = "squad_upi_qr.png"
    if os.path.exists(qr_path):
        with open(qr_path, "rb") as qr_file:
            await update.message.reply_photo(photo=qr_file, caption="📷 पेमेंट का Screenshot भेजें।")
    else:
        await update.message.reply_text("⚠️ QR कोड नहीं मिला।")

# ✅ Screenshot handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.forward(chat_id=ADMIN_ID)
    await update.message.reply_text("✅ Screenshot भेज दिया गया है। हमारी टीम बहुत जल्द आपसे संपर्क करेगी।")

# ✅ Admin approval
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        if context.args:
            user_id = int(context.args[0])
            await context.bot.send_message(chat_id=user_id, text=f"✅ पेमेंट कन्फर्म हो गया है!\nयह रहा ग्रुप लिंक:\n{GROUP_LINK}")
            await update.message.reply_text("📨 Link भेज दिया गया ✅")
        else:
            await update.message.reply_text("❌ User ID नहीं मिला.\nउदाहरण: /approve 123456789")

# ✅ Bot Setup
if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("approve", approve))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app_bot.run_polling()
