import os
import psutil
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

# ---------------- Flask App ----------------
web = Flask(__name__)

@web.route("/")
def home():
    return "✅ Web service running. Telegram bot active."

# ---------------- Telegram Handlers ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot is online!\nUse /stats to see RAM & CPU usage."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()

    await update.message.reply_text(
        f"📊 *System Stats*\n\n"
        f"🧠 CPU: `{cpu}%`\n"
        f"💾 RAM: `{mem.percent}%`\n"
        f"📦 Used: `{mem.used / 1024**3:.2f} GB`\n"
        f"📀 Total: `{mem.total / 1024**3:.2f} GB`",
        parse_mode="Markdown"
    )

# ---------------- Run Bot ----------------
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()

# ---------------- Main ----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    web.run(host="0.0.0.0", port=PORT)
