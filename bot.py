import os
import psutil
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "✅ Bot is running (Web Service active)"

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()

    total_ram = mem.total / (1024 ** 3)
    used_ram = mem.used / (1024 ** 3)

    msg = (
        "📊 *System Stats*\n\n"
        f"🧠 CPU: `{cpu}%`\n"
        f"💾 RAM: `{mem.percent}%`\n"
        f"📦 Used: `{used_ram:.2f} GB`\n"
        f"📀 Total: `{total_ram:.2f} GB`"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bot is live!\nUse /stats to check RAM & CPU."
    )

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app_web.run(host="0.0.0.0", port=PORT)
