from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import threading
import os

# 🟢 Flask web server (for UptimeRobot)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive!"

def start_flask():
    app.run(host='0.0.0.0', port=8080)

# 🟢 Telegram Bot Details
BOT_TOKEN = "7588601306:AAHovG-BWMOm3rs9k94rMDmPrTpREIBY-R8"
ADMIN_ID = 7881285373
GROUP_LINK = "https://t.me/+HGrIvWqrAkw1OGU1"
UPI_ID = "squad.support@ibl"

# 🟢 Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Namaste {update.effective_user.first_name}!\n"
        f"💸 Pay ₹100 at `{UPI_ID}` and send screenshot.",
        parse_mode="Markdown"
    )
    if os.path.exists("squad_upi_qr.png"):
        with open("squad_upi_qr.png", "rb") as file:
            await update.message.reply_photo(photo=file, caption="📸 Scan this QR")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.forward(chat_id=ADMIN_ID)
    await update.message.reply_text("✅ Screenshot sent to Admin.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID and context.args:
        user_id = int(context.args[0])
        await context.bot.send_message(chat_id=user_id, text=f"✅ Payment confirmed!\nJoin group: {GROUP_LINK}")
        await update.message.reply_text("✅ Sent.")
    else:
        await update.message.reply_text("❌ /approve <user_id> likho")

# 🟢 Bot Starter
def start_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("approve", approve))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🤖 Bot is running...")
    app_bot.run_polling()

# 🟢 Run Flask + Bot together
if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    start_bot()
