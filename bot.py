import os
import psutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()

    total_ram = mem.total / (1024 ** 3)
    used_ram = mem.used / (1024 ** 3)
    ram_percent = mem.percent

    msg = (
        "📊 *System Stats*\n\n"
        f"🧠 CPU Usage: `{cpu}%`\n"
        f"💾 RAM Usage: `{ram_percent}%`\n"
        f"📦 Used RAM: `{used_ram:.2f} GB`\n"
        f"📀 Total RAM: `{total_ram:.2f} GB`"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bot is running!\nUse /stats to see RAM & CPU usage."
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))

    print("Bot started...")
    app.run_polling()
