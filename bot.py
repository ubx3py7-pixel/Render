import os
import psutil
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

# ---- Flask app (keeps Render Web Service alive) ----
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Web service is running. Telegram bot active."

# ---- Telegram bot handlers ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot is live!\nUse /stats to check RAM & CPU."
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()

    msg = (
        "📊 *System Stats*\n\n"
        f"🧠 CPU Usage: `{cpu}%`\n"
        f"💾 RAM Usage: `{mem.percent}%`\n"
        f"📦 Used RAM: `{mem.used / 1024**3:.2f} GB`\n"
        f"📀 Total RAM: `{mem.total / 1024**3:.2f} GB`"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")

# ---- Run Telegram bot ----
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    await app.initialize()
    await app.start()
    await app.bot.initialize()
    await app.stop()  # keep polling alive
    await app.run_polling()

# ---- Main entry ----
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    flask_app.run(host="0.0.0.0", port=PORT)
