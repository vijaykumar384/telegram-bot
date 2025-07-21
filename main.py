from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import os
import threading

# 🔹 Flask web server (for uptime)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 🔹 Bot configuration
BOT_TOKEN = "7588601306:AAHovG-BWMOm3rs9k94rMDmPrTpREIBY-R8"
ADMIN_ID = 7881285373
GROUP_LINK = "https://t.me/+HGrIvWqrAkw1OGU1"
UPI_ID = "squad.support@ibl"

# 🔹 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Namaste {update.effective_user.first_name}!\n"
        f"💰 Group join karne ke liye ₹100 ka payment karo.\n"
        f"📥 UPI ID: `{UPI_ID}`\n"
        "📷 Payment ke baad screenshot bhejo.",
        parse_mode="Markdown"
    )
    if os.path.exists("squad_upi_qr.png"):
        with open("squad_upi_qr.png", "rb") as qr:
            await update.message.reply_photo(photo=qr, caption="📸 Yeh raha QR code")

# 🔹 Screenshot handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.forward(chat_id=ADMIN_ID)
    await update.message.reply_text("✅ Screenshot admin ko bhej diya gaya hai.")

# 🔹 Admin approval
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID and context.args:
        user_id = int(context.args[0])
        await context.bot.send_message(chat_id=user_id, text=f"✅ Payment confirmed!\nGroup link: {GROUP_LINK}")
        await update.message.reply_text("📨 User ko group link bhej diya.")
    else:
        await update.message.reply_text("❌ /approve <user_id> likho")

# 🔹 Start bot & Flask
def start_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("approve", approve))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app_bot.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # Flask ko alag thread me chalao
    start_bot()  # Bot start karo
