import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot chal raha hai ✅ Railway se!")

TOKEN = os.getenv("8391838423:AAHQ8PNOBRb51M15v6Br9QpD79422pg3hIs")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running on Railway ✅")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
