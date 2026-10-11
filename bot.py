import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from groq import Groq

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = "8895763568:AAHwEwbEerZ4W11OCRApE3LX_eCsY784x8k"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# هندلر دستور استارت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من هوش مصنوعی بصیر هستم. هر سوالی داری از من بپرس جگر!")

# هندلر پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "تو یک هوش مصنوعی بسیار مهربان، هوشمند و صمیمی به نام بصیر هستی که به زبان فارسی و دری پاسخ می‌دهی.",
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        ai_response = chat_completion.choices[0].message.content
    except Exception as e:
        ai_response = f"متأسفانه خطایی رخ داد: {e}"

    await update.message.reply_text(ai_response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # اضافه کردن دستور /start و پیام‌های متنی
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("ربات تلگرام بصیر با موفقیت روشن شد و آماده پاسخگویی است...")
    application.run_polling()
    