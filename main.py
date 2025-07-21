from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import os
import threading

# ✅ Web server for UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

keep_alive()

# ✅ Bot Config
BOT_TOKEN = "7588601306:AAHovG-BWMOm3rs9k94rMDmPrTpREIBY-R8"
ADMIN_ID = 7881285373
GROUP_LINK = "https://t.me/+HGrIvWqrAkw1OGU1"
UPI_ID = "squad.support@ibl"

# ✅ Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Namaste {user.first_name}!\n\n"
        f"💸 UPI ID: `{UPI_ID}`\n"
        "📷 Payment ke baad screenshot bhejo.\n"
        "👇 QR code niche diya gaya hai:",
        parse_mode="Markdown"
    )
    qr = "squad_upi_qr.png"
    if os.path.exists(qr):
        with open(qr, "rb") as file:
            await update.message.reply_photo(photo=file, caption="QR Code for Payment")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.forward(chat_id=ADMIN_ID)
    await update.message.reply_text("✅ Screenshot bhej diya gaya hai Admin ko.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        if context.args:
            user_id = int(context.args[0])
            await context.bot.send_message(chat_id=user_id, text=f"✅ Payment Confirmed!\nHere is the group link:\n{GROUP_LINK}")
            await update.message.reply_text("📨 Link bhej diya gaya.")
        else:
            await update.message.reply_text("❌ User ID nahi diya.\nExample: /approve 123456789")

# ✅ Main Bot Starter
if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("approve", approve))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    app_bot.run_polling()
